# Docker安装和使用Ciphey自动解码器和解密器

Ciphey 旨在自动识别和解码/解密常见的编码和加密技术，如其文档中所述。它由 Brandon Skerritt 创建，并获得 MIT 许可。据作者介绍，该工具使用“自然语言处理和人工智能，以及一些常识”。

项目地址：[Ciphey](https://github.com/Ciphey/Ciphey)

安装Ciphey：

```bash
docker pull remnux/ciphey
```

要使用此 Docker 容器运行 Ciphey，请创建一个目录（例如 ~/workdir），您将在其中存储输入文件（例如 input.txt）。然后，使用这样的命令来运行 Ciphey 并将您的目录映射到容器中：

```bash
docker run -it --rm -v ~/workdir:/home/nonroot/workdir remnux/ciphey -f input.txt 
```

或者对于命令行运行的文本输入：

```bash
docker run -it --rm remnux/ciphey "=MXazlHbh5WQgUmchdHbh1EIy9mZgQXarx2bvRFI4VnbpxEIBBiO4VnbNVkU"
```

