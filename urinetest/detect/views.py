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
        
        image = request.FILES.get('image')

        if not  image:
            return Response({'error': 'image data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            image = Image.open(image)
            colors_extracted = extract_colors(image)
        except Exception as e:
            return Response({'error': f'Error processing image: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        d = ['URO', 'BIL', 'KET', 'BLD', 'PRO', 'NIT', 'LEU', 'GLU', 'SG', 'PH']

        # Create dictionary with colors in the order of the 'd' list
        colo = {key: colors_extracted[i] for i, key in enumerate(d)}
        print(colo)

        return JsonResponse(colo)



