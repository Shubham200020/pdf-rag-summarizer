import fitz  # PyMuPDF
import io
import base64
from typing import List
from PIL import Image
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import config

# Optional pytesseract import with fallback
try:
    import pytesseract
    HAS_PYTESSERACT = True
except ImportError:
    HAS_PYTESSERACT = False

class ImageService:
    """Service to extract images, OCR embedded text inside images, and generate vector-embeddable descriptions."""
    
    @staticmethod
    def extract_and_caption_images(pdf_path: str, api_key: str = None) -> List[Document]:
        """
        Extracts images from PDF pages.
        1. If the image contains text (scanned text/diagrams with labels), performs OCR to extract text.
        2. If the image is a picture/figure, generates a visual description of what the picture contains.
        """
        key = api_key or config.OPENAI_API_KEY
        file_name = fitz.os.path.basename(pdf_path) if hasattr(fitz, 'os') else pdf_path.split("/")[-1].split("\\")[-1]
        
        image_documents = []
        try:
            doc = fitz.open(pdf_path)
        except Exception as e:
            print(f"[ImageService] Failed to open PDF for image extraction: {e}")
            return []

        llm_vision = None
        if key and key != "your_openai_api_key_here":
            try:
                llm_vision = ChatOpenAI(model="gpt-4o-mini", temperature=0.1, openai_api_key=key)
            except Exception:
                pass

        total_extracted = 0
        for page_index in range(len(doc)):
            page = doc[page_index]
            page_num = page_index + 1
            image_list = page.get_images(full=True)
            
            for img_index, img_info in enumerate(image_list[:5]):  # Process top 5 images per page
                xref = img_info[0]
                try:
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"]
                    width = base_image["width"]
                    height = base_image["height"]
                    
                    # Filter out tiny icon/bullet images (< 50x50 pixels)
                    if width < 50 or height < 50:
                        continue
                        
                    total_extracted += 1
                    pil_img = Image.open(io.BytesIO(image_bytes))
                    
                    ocr_text = ""
                    # 1. Extract text inside image using PyTesseract OCR if available
                    if HAS_PYTESSERACT:
                        try:
                            extracted = pytesseract.image_to_string(pil_img).strip()
                            if len(extracted) > 10:
                                ocr_text = extracted
                        except Exception as ocr_err:
                            print(f"[ImageService] OCR extraction notice: {ocr_err}")
                            
                    content_str = ""
                    
                    # 2. Vision AI description (If text inside image, extracts text; if picture, describes what it is)
                    if llm_vision:
                        try:
                            b64_img = base64.b64encode(image_bytes).decode('utf-8')
                            msg = HumanMessage(content=[
                                {"type": "text", "text": (
                                    "Analyze this image from a PDF:\n"
                                    "1. If it contains text, OCR/transcribe ALL text inside the image word-for-word.\n"
                                    "2. If it is a picture, diagram, or chart, describe clearly WHAT THE PICTURE SHOWS and what it is."
                                )},
                                {"type": "image_url", "image_url": {"url": f"data:image/{image_ext};base64,{b64_img}"}}
                            ])
                            vision_res = llm_vision.invoke([msg])
                            content_str = f"[Image Content & Description on Page {page_num}]: {vision_res.content}"
                        except Exception as ve:
                            print(f"[ImageService] Vision AI fallback: {ve}")
                            
                    if not content_str:
                        if ocr_text:
                            content_str = f"[Extracted Text inside Image on Page {page_num}]: {ocr_text}"
                        else:
                            content_str = f"[Picture/Figure on Page {page_num}]: Figure {total_extracted} ({width}x{height} {image_ext.upper()} image)."

                    doc_obj = Document(
                        page_content=content_str,
                        metadata={
                            "source_file": file_name,
                            "page_label": page_num,
                            "content_type": "embedded_image_content",
                            "image_dimensions": f"{width}x{height}"
                        }
                    )
                    image_documents.append(doc_obj)
                    
                except Exception as ex:
                    print(f"[ImageService] Skipping image xref {xref}: {ex}")
                    
        print(f"[ImageService] Successfully extracted and indexed {len(image_documents)} image contents & text.")
        return image_documents
