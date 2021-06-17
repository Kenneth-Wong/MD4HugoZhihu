## 腾讯COS图床+Hugo部署个人Blog+知乎一站式解决方案

### 典型配置方案


- 使用typora编辑博客文档；
- 使用腾讯云COS作为图床；
- 使用Hugo（[Academia项目](https://wowchemy.com/docs/getting-started/)）部署个人Blog（参考其官方文档可以方便地建立起个人静态网站）；
- 知乎发布文章。
- 详细代码请前往[Kenneth-Wong/MD4HugoZhihu](https://github.com/Kenneth-Wong/MD4HugoZhihu)，觉得好可以留下一星哈



### 使用方法

- 环境：
  - 暂时仅支持Linux/MacOS，py3.6+

- 腾讯云COS python API安装：

  ```shell
  pip install -U pip install -U cos-python-sdk-v5
  ```

  也有其他方案使用github作为图床，但国内访问github不稳定，因此推荐使用腾讯云COS作为图床。

- 使用typora编辑Markdown并上传资源，修改资源路径

  - 一般会涉及到图片等一些外部资源。为文档和外部资源建立路径如下（以本项目中的rnn为例）：

    ```shell
    rnn
    ├── a.md
    ├── rnn
    	├── x.jpg
    	...
    ```

    文档中可以插入图片时以相对路径的方式插入：

    ```markdown
    ![插入图释](rnn/x.jpg)
    ```

  - 调用cos\_remote.py脚本将rnn/下的图片全部上传，并且将文档中的所有图片路径转换为url路径。注意需要先将脚本中的私密信息先替换成你自己的。（腾讯云COS中可以查到）

    ```shell
    python cos_remote.py u --dir rnn/rnn --doc a.md
    ```

    该脚本会将图片上传到图床，最后生成一个a_urls.md文件。

- 转换成适配Hugo的文档（可选）

  - 如果需要将文档上传到Hugo个人静态网站，需要做一些修改。Hugo中的Markdown对于下划线（包括公式中）有特别解释，因此需要转义。一般我们写公式下标时直接写“\_”就够了，但是在Hugo需要写成“\\_”。另外，换行“\\\\”需要写成“\\cr”。该脚本就是完成这两个任务。生成一个a\_blog.md文档

    ```shell
    python toblog.py a.md 
    ```

- 转换到知乎（可选）

  - 知乎对公式处理貌似有不同的处理，本项目参考[miracleyoo/Markdown4Zhihu](https://github.com/miracleyoo/Markdown4Zhihu)对文档进行替换，生成一个a\_zhihu.md文档。

    ```
    python tozhihu.py a.md
    ```

    

