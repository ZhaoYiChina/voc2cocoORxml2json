# voc2cocoORxml2json
数据集转换工具，将voc2007格式的数据集，转换为coco2017格式的数据集。

具体使用的是 parseXmlFiles方法，直接用标注好的xml格式的文件，进行处理。

处理过程：新格式中image的重新编排，annotations的重新编排。

注意要点：
1. annotation中需要image_id, 对应的是imageset中的id。

最终的images格式
{"id": 0, "file_name": "000000.jpg", "width": 768, "height": 576}

最终的annotations格式
{"segmentation": [[404, 203, 404, 261, 490, 261, 490, 203]], "area": 4988, "iscrowd": 0, "ignore": 0, "image_id": 0, "bbox": [404, 203, 86, 58], "category_id": 0, "id": 0}


新的数据还有categories格式内容
{"supercategory": "none", "id": 0, "name": "xxx"}