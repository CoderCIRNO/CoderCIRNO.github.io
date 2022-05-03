# YUV图片格式

YUV是图片、相机、视频中会用到的一种图像格式，Y(Luminance)表示亮度，U(Chrominance)表示色度，V(Chroma)表示浓度。

YUV根据Y、U、V在水平、垂直方向的采样率之比又分为yuv444、yuv422和yuv420，不同的格式存储方式也略有不同，本文我们以yuv420为例。

yuv420格式中，Y和UV在水平和垂直方向采样率之比都是2：1，这意味着yuv420一定会损失部分色彩信息。

Y、U、V分量的存储空间占用比为4:1\:1，存储顺序则是按像素从左到右横向扫描，先存储所有Y分量，再存储所有U分量，最后存储所有V分量，每个分量占一个字节，也就是8bit。

如果有一个4x4的yuv420p图片，其24B存储空间的大致分布将如下所示：

| **Y** | **Y** | **Y** | **Y** |
| ----- | ----- | ----- | ----- |
| **Y** | **Y** | **Y** | **Y** |
| **Y** | **Y** | **Y** | **Y** |
| **Y** | **Y** | **Y** | **Y** |
| **V** | **V** | **V** | **V** |
| **U** | **U** | **U** | **U** |

Y分量占据了16个字节，U、V分量分别占据4个字节。并不需要知道这些UV是如何反映到每个像素上的，知道大致存储结构就已经可以对图像进行消色操作了。

如果我们只获取Y分量，那么我们就能得到一副黑白画面，如果除Y分量还额外获取UV分量，就能得到彩色画面。这也是为什么电视信号能同时兼容彩电和黑白电视，因为电视信号就是用这种存储方式传输画面。

## **生成与查看YUV图片**

要转换yuv格式和查看yuv图片，需要安装ffmpeg。

yuv格式并没有文件头，无法从文件内容中获知图片尺寸信息，必须人为指定。

因此建议在命名yuv文件时，在文件名中注明图片尺寸，以便后续使用。

```bash
#安装ffmpeg
$ sudo apt install ffmpeg
 
#将图片尺寸为384x182的TestPic.png转换为yuv420格式的图片out_384x182.yuv
$ ffmpeg -i TestPic.png -s 384x182 -pix_fmt yuv420p out_384x182.yuv
 
#查看尺寸为384x182的yuv格式图片out_384x182.yuv
$ ffplay -f rawvideo -video_size 384x182 out_384x182.yuv
```

## **图像消色实验**

通过C++的文件读写操作，可以很轻易的按字节操作yuv文件。

用 **0x80** （-128）覆盖UV分量即可消除对应的色彩信息。

```cpp
#include<iostream>
#include<iomanip>
#include<fstream>
#include<thread>
#include<string.h>
#include<string>
#include<dirent.h>
#include<vector>
#include<utility>
#include<chrono>
#include<cstdlib>
#include<unistd.h>

#include <android/log.h>
#include <utils/CallStack.h>

//<utils/CallStack.h> refers <log/log.h>, in <log/log.h> defined  LOG_TAG to NULL
#undef LOG_TAG
#define LOG_TAG "wangtianlin1"
#define LOGD(...) __android_log_print(ANDROID_LOG_DEBUG,LOG_TAG ,__VA_ARGS__)
#define LOGI(...) __android_log_print(ANDROID_LOG_INFO,LOG_TAG ,__VA_ARGS__)

const uint WIDTH = 1844;
const uint HEIGTH = 4000;
const uint BUFFER_CAPACITY = 256;

const std::string INPUT_FOLDER = "input//";
const std::string OUTPUT_FOLDER = "output//";
const uint8_t FILE_TYPE_NUM = 8;

android::CallStack g_callStack;
void dump_stack_android(void)
{
        g_callStack.update();
        g_callStack.log(LOG_TAG);
}

class DataQueue{
public:
    DataQueue(){
        this->head = nullptr;
        this->tail = nullptr;
        this->readDone = false;
        this->writeDone = false;
    }
    //Add a node at queue tail.
    void Product(char* inputData, uint inputLength){
        if (!tail){
            this->tail = new DataNode(inputData, inputLength);
            this->head = this->tail;
        }else{
            this->tail->_next = new DataNode(inputData, inputLength);
            this->tail = this->tail->_next;
        }
    }
    //Get a node at queue head and delete it, if head is null, keep waitting.
    std::pair<char*, uint> Consume(){
        //Consumer is allowed to wait.
        while(!this->head);
        std::pair<char*, uint> result((char*)this->head->_data, this->head->_length);
        DataNode* temp = (DataNode*)this->head;
        //Another wait.
        while(!this->head->_next && !this->readDone);
        /*///////////////////////////////////////////////////////////////////////////////////////////////
        //
        //    Three situations : (next) || (done) || (next && done)
        //    next: strill reading.
        //    done: read finished and data is empty. Writting should stop at this situation.
        //    next && done: read finished but data is not empty.
        //
        ///////////////////////////////////////////////////////////////////////////////////////////////*/
        if(this->head->_next){
            this->head = temp->_next;
        }else{
            //read done and write done.
            this->writeDone = true;
            LOGD("Child Thread - Write Finished.\n");
            dump_stack_android();
        }
        delete(temp);
        return result;
    }
    void SetReadDone(){
        this->readDone = true;
    }
    bool IsWriteDone(){
        return (bool)this->writeDone;
    }
private:
    struct DataNode{
        char* volatile _data;
        volatile uint _length;
        DataNode* volatile _next;
        DataNode(char* inputData, uint inputLength){
            _data = inputData;
            _length = inputLength;
            _next = nullptr;
        }
    };
    DataNode* volatile head;
    DataNode* volatile tail;
    volatile bool readDone;
    volatile bool writeDone;
};

DataQueue* g_DQ = new DataQueue();

//Open INPUT_FOLDER and create a string vector by all files
void CreateFileNameVector(std::vector<std::string> &inputStringVector){
    DIR* dir;
    struct dirent* ptr;
    std::string path = "input//";
    if(NULL == (dir = opendir(path.c_str()))){
        LOGI("Main  Thread - No input file found!\n");
        exit(1);
        return;
    }
    while((ptr = readdir(dir)) != NULL){
        if(FILE_TYPE_NUM == ptr->d_type){
            std::string temp = ptr->d_name;
            inputStringVector.push_back(temp);
        }
    }
    return;
}
//Read BUFFER_CAPACITY Byte once from yuv file and deliver it to writer thread, skip -
//color informations(UV).
void PicDataRead(void){
    const uint ReadByteNum = WIDTH * HEIGTH;
    std::vector<std::string> fileNames;
    CreateFileNameVector(fileNames);

    for(const std::string &currentFileName : fileNames){
        std::ifstream picReader(INPUT_FOLDER + currentFileName, std::ifstream::binary);

        char* _temp = new char[currentFileName.size()];
        strcpy(_temp, currentFileName.c_str());

        picReader.seekg(0, picReader.end);
        const uint PicSize = picReader.tellg();
        picReader.seekg(0, picReader.beg);
        g_DQ->Product(_temp, PicSize - ReadByteNum);

        LOGD("Main  Thread - File %s reading...\n", currentFileName.c_str());
        for(uint readCounter = 0; readCounter < ReadByteNum;){
            uint _bufferLeft = ReadByteNum - readCounter;
            uint _currentBufferSize = BUFFER_CAPACITY;
            if(_bufferLeft < BUFFER_CAPACITY){
                _currentBufferSize = _bufferLeft;
            }
            char* inputData = new char[_currentBufferSize];
            picReader.read(inputData, _currentBufferSize);
            g_DQ->Product(inputData, _currentBufferSize);
            readCounter += _currentBufferSize;
        }
        picReader.close();
        LOGD("Main  Thread - File %s reading done!\n", currentFileName.c_str());
    }
    g_DQ->SetReadDone();
    LOGD("Main  Thread - Read Finished!\n");
    return;
}

//Write information received to file, and fill color information with 0x80.
void PicDataWrite(void){
    const uint WriteByteNum = WIDTH * HEIGTH;
    char* grayBuffer = new char[BUFFER_CAPACITY];
    memset(grayBuffer,0x80,BUFFER_CAPACITY);
    while(true){
        LOGD("Child Thread - Getting file name and bufferLeftNum...\n");
        std::pair<char*, uint> resultReceiver = g_DQ->Consume();
        std::string currentFileName(resultReceiver.first);
        const uint bufferLeftNum = resultReceiver.second;
        LOGD("Child Thread - File name: %s\n",  currentFileName.c_str());
        delete[](resultReceiver.first);
        std::ofstream picOutput(OUTPUT_FOLDER + currentFileName, std::ofstream::binary);

        LOGD("Child Thread - File %s writing...\n", currentFileName.c_str());
        for(uint writeCounter = 0; writeCounter < WriteByteNum;){
            resultReceiver = g_DQ->Consume();
            picOutput.write(resultReceiver.first, resultReceiver.second);
            delete[](resultReceiver.first);
            writeCounter += resultReceiver.second;
        }

        for(uint writeCounter = 0; writeCounter < bufferLeftNum;){
            uint _bufferLeft = bufferLeftNum - writeCounter;
            uint _currentBufferSize = BUFFER_CAPACITY;
            if(_bufferLeft < BUFFER_CAPACITY){
                _currentBufferSize = _bufferLeft;
            }
            picOutput.write(grayBuffer, _currentBufferSize);
            writeCounter += _currentBufferSize;
        }
        picOutput.close();
        LOGD("Child Thread - File %s writing done!\n", currentFileName.c_str());

        if(g_DQ->IsWriteDone()){
            LOGD("Child Thread - All file processed!\n");
            break;
        }
    }
    delete[](grayBuffer);
    return;
}

int main(void){
    const std::chrono::system_clock::time_point startTime = std::chrono::system_clock::now();
    LOGD("Main  Thread - #######Start#######\n");

    std::thread t_writer(PicDataWrite);
    PicDataRead();
    LOGD("Main  Thread - Waitting child thread...\n");
    t_writer.join();

    const std::chrono::system_clock::time_point endTime = std::chrono::system_clock::now();
    const auto duration = std::chrono::duration_cast<std::chrono::microseconds>(endTime - startTime).count();
    LOGD("Main  Thread - All time consumed %.3f  ms\n", duration * 1e-3);
    LOGD("Main  Thread - ####### End #######\n");
}

```
