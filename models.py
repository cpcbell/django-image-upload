import os.path
from django.db import models
from django.conf import settings

def get_upload_to(instance, filename):

	return instance.get_upload_to_path(filename)

# Create your models here.

class ImageTypeManager(models.Manager):

	def get_image_type(self, imageType):

		try: 
			return self.get(name=imageType)
		except:

			try:
				return self.get(name='generic')
			except:
				self.create(name='generic')
				return self.get(name='generic')

		return None

class ImageType(models.Model):

	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)

	objects = ImageTypeManager()

	def __unicode__(self):
		return self.name

class ImageStorageManager(models.Manager):

	def get_upload_path(self, name):

		return settings.MEDIA_ROOT+str(name)

	def get_file_size(self, modelInstance):

		try:
			return os.path.getsize(self.get_upload_path(modelInstance.img.name)) 
		except:
			return False

	def get_file_mimetype(self, modelInstance):

		try:
			import magic

			return magic.from_file(self.get_upload_path(modelInstance.img.name), mime=True)
		except:
			return False



	def get_file_extension(self, name):

		try:
			fileNameAry = str(name).split('.')

			return '.'+fileNameAry[-1]
		except:
			return False

	def create_unique_filename(self):

		import time
	
		return str(time.strftime('%s')) 

	def new_upload_name(self, modelInstance):
	
		currentPath = settings.MEDIA_ROOT+modelInstance.img.name
	
		fileExt = self.get_file_extension(modelInstance.img.name)

		if fileExt == False:
			return None

		thisNewName = self.create_unique_filename()+fileExt

		newPath = settings.MEDIA_ROOT+thisNewName

		try:
			os.rename(currentPath,newPath)
			return thisNewName 
		except:
			return None

	def upload_too_big(self, modelInstance):

		if int(modelInstance.fileSize) > settings.MAX_UPLOAD_SIZE:
			return True 

		return False

	def allowed_upload_image(self, modelInstance):

		if modelInstance.fileType in settings.ALLOWED_IMAGE_TYPES:
			return True

		return False


	def save_file_upload(self, modelInstance, imageTypeObj, checkFileType=False):

		modelInstance.imgType = imageTypeObj 
            	modelInstance.save()

		modelInstance.fileSize = self.get_file_size(modelInstance) 

		if self.upload_too_big(modelInstance):

			reason = 'File size was: ' +  str(modelInstance.fileSize)
			errorObj = {'error':True,'reason':reason}

			modelInstance.delete()
			return errorObj

		if checkFileType == True:

			modelInstance.fileType = self.get_file_mimetype(modelInstance) 

			if self.allowed_upload_image(modelInstance) == False:
				
				reason = 'File type was: ' +  modelInstance.fileType
				errorObj = {'error':True,'reason':reason}

				modelInstance.delete()
				
				return errorObj 

		return modelInstance

	def unique_rename_file_upload(self, modelInstance):

		currentPath = self.get_upload_path(modelInstance.img.name)

		newName = self.new_upload_name(modelInstance)

		if newName == False:
			return None

		newPath = self.get_upload_path(newName)

		modelInstance.img = newName 
		modelInstance.save()

		return modelInstance 

class ImageStorage(models.Model):

	name = models.CharField(max_length=200)
	description = models.TextField(blank=True)

	img = models.FileField(upload_to=get_upload_to,blank=True,null=True)
    	imgType = models.ForeignKey(ImageType, blank=True, null=True, on_delete=models.SET_NULL)

	src = models.CharField(max_length=500,blank=True)

	objects = ImageStorageManager()

	def get_upload_to_path(instance, filename):
    		return filename

	def __unicode__(self):
		return self.name

