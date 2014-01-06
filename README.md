django-image-upload
===================

Upload images and make them available to Django

This image upload model will check file size, file extension and give the upload a unique file name on the filesystem.

File extension detection uses magic package.

The view shows a simple example of how to use the model. There is a simple template upload.html that goes with the example.

An example of urls.py is included that goes with the view.

Add these constants to your settings.py:

MAX_UPLOAD_SIZE = 150100

ALLOWED_IMAGE_TYPES = ['image/png','image/jpeg','image/gif']

Thanks,

Clay
