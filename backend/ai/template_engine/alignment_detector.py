"""
Alignment Detector
"""


class AlignmentDetector:


    def detect(self,blocks):


        if not blocks:

            return "unknown"



        positions=[]


        for block in blocks:


            bbox=block["bbox"]


            x=bbox[0][0]

            positions.append(x)



        avg=sum(positions)/len(positions)



        if avg < 800:

            return "left"


        elif avg <1500:

            return "center"


        else:

            return "right"