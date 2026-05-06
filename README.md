# 2026-YOLO-World-MMKit

Forked from [AILab-CVC/YOLO-World](https://github.com/AILab-CVC/YOLO-World).

[switch to Chinese](README-zh.md)

## WHY DO YOU NEED THIS?

I'm using YOLO-World in a small program, but [the official GitHub repo](https://github.com/AILab-CVC/YOLO-World) is very hard to use due to complex dependencies and the outdated mmcv environment. You might say that Ultralytics is an option—and indeed, it's a very convenient and useful platform. You can use it directly and easily via [ultralytics/models/yolo-world/](https://docs.ultralytics.com/zh/models/yolo-world/).

However, when it comes to customizing YOLO-World, we still have to use `mmcv`, `mmengine` and `mmyolo` to load the models and pretrained weights. So in the end, you have to deal with dependencies and the environment.

In this program, I'm trying to change the situation. That is not only making YOLO-World easy-to-use like the model on Ultralytics, but also making it convenient to customize.

## FILES

### My Work

#### Environment

My option is to use docker to install mmcv and I recommand you to use this too, except that you want to learn how to build the environment. You can use ubuntu server or `Windows Subsystem for Linux`(wsl2) to run docker.
- location:[env/](env/)
- readme:[here](env/readme.md)

#### Configs

Due to the change of the file structure, I edit some of config files to make them more flexible.
- location:[configs](configs/)
- readme:[here](configs/readme.md)

Futhermore, I move the class_text_path to the configs folder too. 
- location:[configs/data_text_json](configs/data_text_json/)
- readme:[here](configs/data_text_json/readme.md)

### Original Work

I save all the original code to admire the contribution of the YOLO-World team.
- location:[Original](Original/)
- readme:[here](Original/readme.md)
- mydetail(you must see it):[here](Original/originaldetail.md)