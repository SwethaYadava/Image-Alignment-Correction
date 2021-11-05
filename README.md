# Image Alignment Correction

An AI method is shown here to determine the alignment of scanned images with the horizontal and vertical axes and, if necessary, correct the alignment.

# Description

After going over the misaligned images folder, i discovered that the images were skewed and rotated, thus this solution will have two stages: first, a skew correction on the original input image, and then an orientation correction on the skew corrected image to produce the final output image.

Stage 1 - Text Skew Correction
In this stage OpenCV and the cv2 techniques will be used. Our input images include dark text on a light backdrop; however, in order to perform the text skew correction method, we must first flip the image (the text is now light on a dark background – we need the inverse). The image is subsequently binarized using a thresholding procedure. We can now compute the minimal rotational bounding box that contains the text sections using this thresholded image. Find all (x, y)-coordinates that are part of the foreground in the thresholded image. These coordinates are passed to cv2.minAreaRect, which calculates the smallest rotating rectangle that encompasses the whole text region. The angle values returned by the cv2.minAreaRect function are in the range [-90, 0]. Use cv2.getRotationMatrix2D to get the centre coordinates and rotation angle. The actual transformation on the input image to rectify the skewness is subsequently performed using this rotation matrix M.

Stage 2 - Image Orientation Correction
Although we might utilise a deep learning strategy to detect and correct the orientation, due to resource constraints we will use pytesseract to automatically detect the orientation angle of a scanned image using the image_to_osd function of tesseract. The function returns the image's orientation in degrees, the rotation angle in degrees if one is required, the orientation confidence, and so on. We will adjust the orientation of the skew corrected image based on the rotation angle detected by pytesseract.


<br/>
<br/>

# Table Of Contents
-  [Project Structure Overview](#project-structure-overview)
-  [Pre requisite](#pre-requisite)
-  [Run python app](#run-python-app)
-  [How to consume an API](#consume-an-api)
-  [Dockerizing an application](#dockerizing-an-application)
-  [Deploy to Kubernetes](#deploy-to-kubernetes)
-  [Resource Analysis](#resource-analysis)
-  [Results](#result)
-  [Version](#version)
-  [Author](#author)
-  [References](#references)

<br/>
<br/>

### Project Structure Overview
```
├──  ImageAlignmentCorrection
│    │
│    └── logger                     - here's the logger package.
│    │    ├── __init__.py
│    │    ├── APILogger.py          - to send non-success code to front-end.
│    │    ├── logger.py             - to log info & error in the code.
│    │    └── LoggerError.py        - to log error while creating a logger object.
│    │
│    └── AlignmentCorrection             - this package is used to get prediction.
│         ├── __init__.py
│         └── AlignmentCorrection.py     - this code reads input and returns the deskewed image.
│    
├── kubernetes                - this folder contains yaml file for deployment.
│   └── deployment.yaml       - Kubernetes YAML file
│
├── client.py                - here's the python API client.
├── Dockerfile               - here's the docker file used to create docker image.
├── README.md                - here's the ReadMe of an application.
├── requirements.txt         - here's the python package requirement txt.
└── run.py                   - here's runnable of an application.
```

<br/>
<br/>

### Pre requisite

Tesseract-OCR - https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-setup-4.00.00dev.exe

Once installed, change the path in ```AlignmentCorrection/AlignmnentCorrection.py``` as follows
```
pytesseract.pytesseract.tesseract_cmd = 'Tesseract-OCR/tesseract.exe'
```

<br/>
<br/>

### Run python app

A step by step series of examples that tell you how to get a development env running for windows os

```
pip install -r requirements.txt
```

Now, you can run project as follows
```
python run.py
```

```
C:\Users\Alice> python run.py
 * Serving Flask app "run" (lazy loading)
 * Environment: production
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
```

<br/>
<br/>

### How to Consume an API

```
POST method:

WebService
--------------------
https://localhost:5000/CorrectAlignment

Header:
------------------------
key:Content-Type
value:application/json

Request:
----------------
{
	"InputImageString": base64 string,
	"InputImageName":"misaligned_img.jpg",
}

Success Response:
----------------
{
    "success": True,
    "AlignmentCorrectedImage": base64 string
}

Error Response:
----------------
SERVER ERROR: (SERVER SIDE ERROR)
{
    "Status_Code": 500,
    "Error": True
}
```

<br/>
<br/>

### Dockerizing an application

##### Docker file
```
For docker file content please refer Dockerfile

```

##### Build the Docker image

Make sure you are in root directory of the project and run the following command.

```
docker build --tag image-alignment-correction-app .
```

The above command will create an app with the tag image-alignment-correction-app

##### Run the docker image we just created

```
docker run --name image-alignment-correction-app -p 5000:5000 image-alignment-correction-app
```
 
##### Commit a container’s file changes or settings into a new image

```
docker commit container-id user-name/image-alignment-correction-app:latest
```

##### Before pushing to docker hub repo login into docker hub using docker account

```
docker login
```

##### Push an image to a registry

```
docker push user-name/image-alignment-correction-app:latest
```

Progress bars are shown during docker push, which show the uncompressed size. The actual amount of data that’s pushed will be compressed before sending, so the uploaded size will not be reflected by the progress bar.

<br/>
<br/>

## Deploy to Kubernetes

I have already wrote a Kubernetes YAML file. Place the following in a file called deployment.yaml under kubernetes folder:

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: image-alignment-correction-app
  namespace: default
spec:
  replicas: 2
  selector:
    matchLabels:
      image-alignment-correction-app: web
  template:
    metadata:
      labels:
        image-alignment-correction-app: web
    spec:
      containers:
      - name: app-site
        image: swethayadava/image-alignment-correction-app:latest
        ports:
        - containerPort: 5000
```

##### Deploy and check your application

1. In a terminal, navigate to where you created deployment.yaml and deploy your application to Kubernetes:
```
kubectl apply -f .\kubernetes\deployment.yaml
```

you should see output that looks like the following, indicating your Kubernetes objects were created successfully:

```
deployment.apps/image-alignment-correction-app created
```

2. Make sure everything worked by listing your deployments:

```
NAME                            READY   UP-TO-DATE   AVAILABLE    AGE
image-alignment-correction-app   2/2     2            2           53m
```

This indicates all one of the pods you asked for in your YAML are up and running.

<br/>
<br/>

## Resource Analysis

Please refer the resource consumption analysis below when executed on two different environments. According to the analysis, to process 10 req/sec, a 12 core CPU with a minimum of 8 GB RAM is required, as memory is not consumed while processing.

Note - Time in sec

<br/>

| CPU |  Memory | #Request (A)  | Execution Time (B) | Execution time per Request | Request per second (A/B) |
|:----:|:----:|:----:|:----:|:----:|:----:|
|4 cores|16 GB|100|64|0.64|1.56|
12 cores|48 GB|100|11|0.11|9.09|


<br/>
<br/>

## Results

<br/>

|Image Type|#|% Images Correctly Aligned|
|---:|:----:|:----:|
|  Rotated |2|1 (50%)|
|  Skewed  |10|9 (90%)|
|  Rotated and Skewed |1|1 (100%)|
| Summary |13|80%|



<br/>
<br/>

## Version

1.0.0 

<br/>

## Author

* **Swetha Yadava** - Initial work and development

<br/>

## References

* [Computer Vision and deep learning](https://github.com/PyImageSearch)
* [Dockerize Flask App](https://www.geeksforgeeks.org/dockerize-your-flask-app/)

