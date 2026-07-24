"""
PDF Template Extractor

Extracts:
- Text
- Coordinates
- Font
- Font size
- Font style
- Alignment information

Used for Batch 5 + Batch 8
"""


import fitz



class PDFTemplateExtractor:



    def extract_layout(self,file_path):


        document = fitz.open(file_path)


        has_text=False



        # Check PDF type

        for page in document:


            text = page.get_text()


            if len(text.strip()) > 50:


                has_text=True

                break



        document.close()



        # Text PDF

        if has_text:


            return self.extract_text_pdf(
                file_path
            )



        # Scanned PDF

        else:


            from .ocr_extractor import OCRExtractor


            ocr = OCRExtractor()


            return ocr.extract_from_pdf(
                file_path
            )





    def extract_text_pdf(self,file_path):


        document = fitz.open(file_path)


        pages=[]



        for page_number,page in enumerate(document):


            blocks=[]



            data = page.get_text(
                "dict"
            )



            for block in data["blocks"]:



                if "lines" not in block:


                    continue




                for line in block["lines"]:



                    for span in line["spans"]:



                        text = span["text"].strip()



                        if not text:


                            continue




                        bbox = span["bbox"]




                        font_name = span.get(
                            "font",
                            "Unknown"
                        )



                        flags = span.get(
                            "flags",
                            0
                        )





                        blocks.append({


                            "text":
                            text,



                            "page":
                            page_number + 1,



                            "bbox":
                            bbox,



                            "x":
                            bbox[0],



                            "y":
                            bbox[1],



                            "width":
                            bbox[2]-bbox[0],



                            "height":
                            bbox[3]-bbox[1],



                            "font":
                            font_name,



                            "font_size":
                            span.get(
                                "size",
                                12
                            ),



                            "bold":
                            "Bold" in font_name,



                            "italic":
                            "Italic" in font_name,



                            "alignment":
                            self.detect_alignment(
                                bbox,
                                page.rect.width
                            ),



                            "flags":
                            flags


                        })





            pages.append({


                "page":
                page_number + 1,


                "blocks":
                blocks


            })





        document.close()




        return {


            "total_pages":
            len(pages),



            "pages":
            pages


        }





    def detect_alignment(self,bbox,page_width):


        x1=bbox[0]

        x2=bbox[2]


        center=(x1+x2)/2



        page_center=page_width/2



        difference = abs(
            center-page_center
        )



        if difference < page_width*0.1:


            return "center"



        elif center > page_center:


            return "right"



        else:


            return "left"