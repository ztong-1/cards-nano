:spades: :hearts: :diamonds: :clubs:

## Introduction
The purpose of this project is to build a tool using NVIDIA Jetson Nano that can play the 24 game. In a 24 game, four cards are placed on the ground facing up and players need to think of an arithmetic way using all four cards in order to reach 24. The allowed operation are just plus, minus, multiplication and division. Unary operation is not allowed. For example, if the four cards are 1,2,3,4, then (1+2+3)*4 would be an acceptable solution. The fastest player wins the game. 

This project contains two main part. In the first part, an objection detection tool will be built to detect and classify the cards seen by the camera. In the second part, if there are four cards detected, then an algorithm will determine if any operation exists to reach 24. The first such solution will be the output.  

## Prerequisite
This project depends on NVIDIA Jetson as the base hardware, so I would recommend completing NVIDIA Jetson Hello AI World tutorial, especially the detection section, in order to be comfortable with understanding the rest.

## Collecting and labelling card images
One way to collect and label card images at once is to continue using the tool provided by the Hello AI World tutorial. If you have never used that tool, I strongly suggest trying at least a couple images. However, one disadvantage is it is hard to modify the resulting .xml files. This makes it difficult to validate labels or to fine tune those bounding boxes previously drawn. 

I ended up separating the collection process and the labelling process. For image collection I used both a Logitech C270 720p webcam and an iPhone 12 Pro. Around 80% of the picture are taken by the webcam at my computer desk and the rest 20% are taken at different locations around the house with diverse background. In Linux, the image capture software I used is Cheese. When taking picture using iPhone, I suggest changing the format from **High Efficiency** (default) to **Most Compatible**, otherwise you will need to find a way to convert those .HEIC images to `.JPG`. After capturing images, I transferred photos to Google Drive and then downloaded to my desktop.

Couple other points to keep in mind are the image size, resolution and orientation. The original images captured by the webcam are 1280*720 with a size ranging from 30 to 130 KB. The original images from iPhone have higher resolution, greater size, different aspect ratio and unknown orientation, depending on your pose when taking the picture. To deal with these discrepancy, in the iPhone camera App, please make sure aspect ratio is set to 16:9 instead of 4:3. I also processed iPhone images via a python script (`process_img.py`) so that they have comparable size and resolution.

I used an open source software called [labelImg](https://github.com/tzutalin/labelImg) for labelling. When labelling, you need to determine what exactly is the object. I included all the non-white element on a card's surface as one single object.

I ended up with around 250 pictures from each category (Ace, 2-10). 

## Data storage
Here is my suggested way of storing both image and annotation data. Suppose on June 10th, 2021 I captured two images using webcam (`2021-06-10-0001.jpg`, `2021-06-10-0002.jpg`) and other two using iPhone (`IMG_100.JPG`, `IMG_1001.JPG`), then I would store them into two separate batches under `img/`. The `annotation/` directory should have exactly the same structure as `img/` does and the only difference is that it stores XML files. 
```
cards-project/
    img/
        batch-061021a/
            2021-06-10-0001.jpg
            2021-06-10-0002.jpg
        batch-061021b/
            IMG_1000.JPG
            IMG_1001.JPG
        batch-061121a/
            2021-06-11-0001.jpg
    annotation/
        batch-061021a/
            2021-06-10-0001.xml
            2021-06-10-0002.xml
        batch-061021b/
            IMG_1000.xml
            IMG_1001.xml
        batch-061121a/
            2021-06-11-0001.xml
```
Storing files in this way makes it easier for future data validation. It also allows me to customize which batch should be included into a particular training session. Remember that the `data/` folder in the tutorial looks like this:
```
data/cards/
    JPEGImages/
        ...
    Annotations/
        ...
    ImagesSets/
        Main/
            trainval.txt
            train.txt
            val.txt
            test.txt
    labels.txt
```
When you are ready to start training, simply copy the chosen image batches to `JPEGImages/` and corresponding annotation batches to `Annotations/`.

I included all images into `trainval.txt`, `train.txt`, but only images taken by webcam into `val.txt`, `test.txt`.

## Training the object detection model
The training process is basically the same as that described in the Hello AI World tutorial. 
Change directory to `jetson-inference/`.
```sh
$ cd jetson-inference/
```
Launch the container. In the training phase, it is OK if the webcam is not connected to Jetson.
```sh
$ docker/run.sh
```
Change directory to `ssd/`, which stands for "Single Shot Multibox Detecter".
```sh
# cd python/training/detection/ssd/
```
Take a look at models sub-directory by using `ls models/`. Any pretrained SSD model (xxx.pth) should be there. If not, you can download these from [here](https://github.com/qfgaohao/pytorch-ssd). In this project, I used both Mobilenet V1 SSD as well as MobileNetV2 SSD-Lite.

If you follow the decription about card images data, you should have all your data ready at `data/cards/`. If you run `ls data/cards/`, you should see three folders, `Annotations/`, `JPEGImages/`, `ImageSets/`, and one text file `labels.txt`. 

Start the training session. The code below starts a training session with MobileNetV2 SSD-Lite as the base model and loads the pretrained version.
```sh
# python3 train_ssd.py --net=mb2-ssd-lite --pretrained-ssd=models/mb2-ssd-lite-mp-0_686.pth --dataset-type=voc --data=data/cards --model-dir=models/cards --batch-size=2 --workers=1 --epochs=30
```
If you want to resume from your own previously saved .pth file, you can replace `--pretrained-ssd=models/mb2-ssd-lite-mp-0_686.pth` with `--resume=models/mb2-ssd-lite-Epoch-n-Loss-xxx.pth`, where `n` is the epoch number and `xxx` is the actual Loss value you encountered. 

The Hello AI World already talks about ways to speed up training. It might also be good practice to restart your machine before firing up a new training session.

In this project, it took approximately 15 minutes to complete one epoch. The validation loss at epoch 0 is 6.9, and it gradually decreased to 1.2 after about 50 epochs.

## Export the model 
Once training is completed, you can export the model to ONNX format.
```sh
# python3 onnx_export.py --net=mb2-ssd-lite --input=models/cards/mb2-ssd-lite-Epoch-n-Loss-xxx.pth --model-dir=models/cards
```
Once again, you need to replace `n` and `xxx` with the actual value. Any normally you would pick the one with the smallest loss. The exported ONNX format model will also be in `models/`.

## Realtime testing
Before heading into 24 game, I want to make sure the detection accuracy is sufficient. If you don't have a webcam connected, you might want to connect it and restart the container. Once done, head back to `ssd/` folder and run the following code.
```sh
# detectnet --model=models/cards/mb2-ssd-lite.onnx --labels=models/cards/labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes --threshold=0.5 /dev/video0
```
If the accuracy seems not acceptable, then please take more picture and re-train the model. One thing to note is that whenever a new onnx model is exported. You want to make sure that `.engine` file is also updated. It seems `detectnet` command only recontruct `.engine` file if there is none exist. Therefore, you may manually remove the old version before running `detectnet` command.

Detection accuracy depends on many factors, including model type, training sample size, number of epochs, precision of bounding box, picture quality, picture diversity, etc. My first attempt wasn't quite successful and the reason could be using SSD mobile-net version 1 and small sample size. The confidence of detected card were typically around 0.4 to 0.5 and some numbers can hardly be detected. After switching to SSD mobile-net version 2, the performance improved a lot. Confidence are usually above 0.85 and the model shows robustness for different card orientation. However, it still had difficulty distinguishing between 8 and 9, 5 and 6. So I increased the sample size a bit more and reached the final trained model.  

## 24 game implementation
No machine learning knowledge is involved in implementing the 24 game. Leetcode has one problem on this game I actually started from [there](https://leetcode.com/problems/24-game/). However, the coding challenge only require outputting whether the card combination has a solution or not. So I added a couple more lines of code so that it outputs actual arithmetic expression.

## Combine 24 game with object detection
Finally, it is now time to crack the 24 game with some AI boost. In the Hello AI World tutorial, a folder called `my-detection/` was created at `Home` directory, and I will use that. Exit the current container by using the command `exit`.

Start the container again, but with mounting the `my-detection/` folder.
```sh
$ docker/run.sh --volume ~/my-detection:/my-detection
```
Execute the following command to start solving 24 game by AI in realtime!
```sh
python3 /my-detection/my-detection.py --model=./python/training/detection/ssd/models/cards/mb2-ssd-lite.onnx --labels=./python/training/detection/ssd/models/cards/labels.txt --input-blob=input_0 --output-cvg=scores --output-bbox=boxes --threshold=0.5
```


