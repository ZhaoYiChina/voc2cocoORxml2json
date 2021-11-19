import xml
import xml.etree.ElementTree as ET
import cv2

"""
实现从xml中读取节点数据，递归遍历所有节点
"""

result_list = []
unique_id = 1

# 遍历所有节点
def walkData(root_node, level, result_list):
    global unique_id
    temp_list = [unique_id, root_node.text]
    if root_node.tag == 'name':
        if len(result_list) != 0:
            hasLabel = False
            for item in result_list:
                if item[1] == root_node.text:
                    hasLabel = True
                    break
            if hasLabel == False:
                result_list.append(temp_list)
                unique_id += 1
        else:
            result_list.append(temp_list)
            unique_id += 1

    # 遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        walkData(child, level + 1, result_list)
    return


# 遍历所有节点
def writeData(tree, root_node, level, result_list, size, file_name):
    global unique_id
    temp_list = [unique_id, root_node.text]
    if root_node.tag == 'size':
        root_node.set('width',size[1])
        root_node.set('height',size[0])
        tree.write(file_name)


    # 遍历每个子节点
    children_node = root_node.getchildren()
    if len(children_node) == 0:
        return
    for child in children_node:
        writeData(tree, child, level + 1, result_list, size, file_name)
    return


def delete_gbk(file_name):
    tree = ET.parse(file_name)
    root = tree.getroot()
    if root != None and root.find('path') != None:
        root.remove(root.find('path'))
        tree.write(file_name)



def getXmlData(file_name, data, train_name):
    tree = ET.parse(file_name)
    root = ET.parse(file_name).getroot()
    if root != None and root.find('size') != None:
        root.remove(root.find('size'))
        size = ET.SubElement(root, 'size')
        width = ET.SubElement(size, 'width')
        width.text = str(data[1])
        height = ET.SubElement(size, 'height')
        height.text = str(data[0])
        depth = ET.SubElement(size, 'depth')
        depth.text = '3'

        root.remove(root.find('filename'))

        name = ET.SubElement(root, 'filename')
        name.text = train_name

        tree = ET.ElementTree(root)
        tree.write(file_name)
    # writeData(tree, root, level, result_list, size, file_name)
    return result_list

if __name__ == '__main__':
    #1001
    for i in range(1001):
        t = 0
        s = '0'
        l = 5 - len(str(i))
        while(l):
            s += '0'
            l -= 1
        pre = 'C:\\Users\\George\\Documents\\Profile\\old project\\ZYproject\\project\\keras-yolo3-object-detection\\VOCdevkit\\VOC2021\\Annotations\\'
        train_name = s + str(i)+ '.jpg'
        img_name = pre + s + str(i) + '.jpg'
        img = cv2.imread(img_name)
        data = img.shape
        file_name = pre + s + str(i) + '.xml'
        R = getXmlData(file_name, data, train_name)

"""
    for x in R:
        print(x)
        pass

    result = ''
    for x in R:
        result_string = "\"" +x[1] + "\"" + ","
        result += result_string
        pass

    print(result)
    
"""