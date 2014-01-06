from django.http import HttpResponse
from django.shortcuts import render_to_response

from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext

from django.conf import settings

from imagestorage.models import ImageType, ImageStorage

# Create your views here.

def saveFileUpload(request, name='image-upload', imageType='generic'):

	message = 'Upload Status: '

	if request.method == 'POST':

		if request.FILES[name]:

           		imgObj = ImageStorage(img=request.FILES[name])

			imgObj.name = str(request.FILES[name])

			imageTypeObj = ImageType.objects.get_image_type(imageType)

			if imageTypeObj == None:
				return HttpResponse(message + 'Failed to find or create generic image type... unexpected error')

			uploadedImgObj = ImageStorage.objects.save_file_upload(imgObj, imageTypeObj, True)

			if isinstance(uploadedImgObj,dict):
				return HttpResponse(message + 'Image did not meet upload criteria or unexpected error. ' + uploadedImgObj['reason'])
		
			fileUploadObj = ImageStorage.objects.unique_rename_file_upload(uploadedImgObj)

			if fileUploadObj == None:
				return HttpResponse(message + 'Image was not renamed properly or unexpected error')

			message = message + fileUploadObj.name + ' Uploaded!'

	return HttpResponse(message)

def blank(request):

	message = 'Upload Status: Ready to Upload an Image!'

	return HttpResponse(message)

def testUpload(request):

	message = None

	return render_to_response('upload.html', 
		{
		'imagePath': settings.MEDIA_URL,
		'message':message,},
		context_instance=RequestContext(request))

