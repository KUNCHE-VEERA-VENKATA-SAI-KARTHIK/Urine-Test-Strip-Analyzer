from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse

from PIL import Image
from sklearn.cluster import KMeans
import numpy as np

def extract_colors(image):
    """
    Extract the dominant colors from the image using KMeans clustering.
    """
    image = image.convert('RGB')  # Ensure image is in RGB mode
    image_array = np.array(image)
    num_pixels = image_array.shape[0] * image_array.shape[1]
    image_array_reshaped = image_array.reshape(num_pixels, -1)
    num_colors = 10
    kmeans = KMeans(n_clusters=num_colors)
    kmeans.fit(image_array_reshaped)
    colors = kmeans.cluster_centers_
    colors = colors.astype(int)
    return [color.tolist() for color in colors]

class TextImageAPI(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        text = request.POST.get('text')
        image = request.FILES.get('image')

        if not text or not image:
            return Response({'error': 'Missing text or image data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Image.open(image)
            colors = extract_colors(image)
        except Exception as e:
            return Response({'error': f'Error processing image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        d = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']

        # Create dictionary with colors in the order of the 'd' list
        colo = {key: colors[i] for i, key in enumerate(d)}

        return JsonResponse(colo)



# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# from PIL import Image
# from sklearn.cluster import KMeans

# def extract_colors(image_path: str):
#     image = Image.open(image_path)
#     image_array = np.array(image)
#     num_pixels = image_array.shape[0] * image_array.shape[1]
#     image_array_reshaped = image_array.reshape(num_pixels, -1)
#     num_colors = 10
#     kmeans = KMeans(n_clusters=num_colors)
#     kmeans.fit(image_array_reshaped)
#     colors = kmeans.cluster_centers_
#     colors = colors.astype(int)
#     result = []
#     for color in colors:
#         result.append(color.tolist())
#     return result

# class TextImageAPI(APIView):    
#     parser_classes = [MultiPartParser, FormParser]

#     def post(self, request):
#         text = request.POST.get('text')
#         image = request.FILES['image']

#         if not text or not image:
#             return Response({'error': 'Missing text or image data'}, status=status.HTTP_400_BAD_REQUEST)

#         # Process the image and extract colors
#         try:
#             image_path = request.FILES['image'].temporary_file_path()
#             colors = extract_colors(image_path)
#         except Exception as e:
#             return Response({'error': f'Error processing image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Return the response with text and extracted colors
#         return Response({'text': text, 'colors': colors})

# @api_view(['GET',"POST"])
# def index1(request):
#     param={'URO': [186, 171, 149],
#             'BIL': [192, 179, 156],
#             'KET': [180, 167, 141],
#             'BLD': [155, 127, 75],
#             'PRO': [170, 155, 99],
#             'NIT': [183, 172, 156],
#             'LEU': [167, 161, 145],
#             'GLU': [134, 160, 148],
#             'SG': [70, 94, 92],
#             'PH': [175, 152, 118]}
#     return Response(param)

# # Create your views here.
# @api_view(['GET','POST'])
# def index1(request):
#     # if request.method == 'POST':
#     #     if 'file' not in request.FILES:
#     #         return JsonResponse({'error': 'Missing image data in request'}, status=400)

#     print(request.POST.get('text'))

    
#     # image = cv2.imread(img_path)
#     # img = cv2.resize(image, (0, 0), fx=1.9, fy=0.9)

#     # # Reading csv file with pandas and giving names to each column
#     # index = ["color", "color_name", "hex", "R", "G", "B"]
#     # file = pd.read_csv('colors.csv', names=index, header=None)

#     # # declaring global variables (are used later on)
#     # clicked = False
#     # r = g = b = x_pos = y_pos = 0

#     # # function to calculate minimum distance from all colors and get the most matching color
#     # def get_color_name(Red, Green, Blue):
#     #     minimum = 16000
#     #     for i in range(len(file)):
#     #         d = abs(Red - int(file.loc[i, "R"])) + abs(Green - int(file.loc[i, "G"])) + abs(
#     #             Blue - int(file.loc[i, "B"]))
#     #         if d <= minimum:
#     #             minimum = d
#     #             colorname = file.loc[i, "color_name"]
#     #     return colorname

#     # # function to get x,y coordinates of mouse moving
#     # def choose_function(event, x, y, flags, param):
#     #     if event == cv2.EVENT_MOUSEMOVE:
#     #         global b, g, r, x_pos, y_pos, clicked
#     #         clicked = True
#     #         x_pos = x
#     #         y_pos = y
#     #         b, g, r = img[y, x]
#     #         b = int(b)
#     #         g = int(g)
#     #         r = int(r)

#     # cv2.namedWindow('colourful_image')
#     # cv2.setMouseCallback('colourful_image', choose_function)

#     # while True:

#     #     cv2.imshow('colourful_image', img)
#     #     if clicked:

#     #         # cv2.rectangle(image, start point, endpoint, color, thickness)-1 fills entire rectangle
#     #         cv2.rectangle(img, (20, 20), (750, 60), (b, g, r), -1)

#     #         # Creating text string to display( Color name and RGB values )
#     #         text = get_color_name(r, g, b) + ' R=' + str(r) + ' G=' + str(g) + ' B=' + str(b)

#     #         # cv2.putText(img,text,start,font(0-7),fontScale,color,thickness,lineType )
#     #         cv2.putText(img, text, (50, 50), 2, 0.8, (255, 255, 255), 2, cv2.LINE_AA)

#     #         # For very light colours we will display text in black colour
#     #         if r + g + b >= 600:
#     #             cv2.putText(img, text, (50, 50), 2, 0.8, (0, 0, 0), 2, cv2.LINE_AA)

#     #         clicked = False

#     #     # Break the loop when user hits 'esc' key
#     #     if cv2.waitKey(20) & 0xFF == 27:
#     #         break

#     # cv2.destroyAllWindows()

#     param={'URO': [186, 171, 149],
#             'BIL': [192, 179, 156],
#             'KET': [180, 167, 141],
#             'BLD': [155, 127, 75],
#             'PRO': [170, 155, 99],
#             'NIT': [183, 172, 156],
#             'LEU': [167, 161, 145],
#             'GLU': [134, 160, 148],
#             'SG': [70, 94, 92],
#             'PH': [175, 152, 118]}
#     return JsonResponse(param)