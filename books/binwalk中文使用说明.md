# binwalk 命令说明中文机翻版

## -B, --signature

这将执行指定文件的签名分析；  如果未指定其他分析选项，则这是默认设置。 

当您希望将签名分析与其他分析器，例如 [--entropy](#entropy):

```bash
$ binwalk --signature firmware.bin

DECIMAL   	HEX       	DESCRIPTION
-------------------------------------------------------------------------------------------------------------------
0         	0x0       	DLOB firmware header, boot partition: "dev=/dev/mtdblock/2"
112       	0x70      	LZMA compressed data, properties: 0x5D, dictionary size: 33554432 bytes, uncompressed size: 3797616 bytes
1310832   	0x140070  	PackImg section delimiter tag, little endian size: 13644032 bytes; big endian size: 3264512 bytes
1310864   	0x140090  	Squashfs filesystem, little endian, version 4.0, compression:lzma, size: 3264162 bytes,  1866 inodes, blocksize: 65536 bytes, created: Tue Apr  3 04:12:22 2012
```

***

## -R, --raw=&lt;string&gt;

这允许您在指定的文件中搜索自定义字符串。  搜索字符串可以包括转义的八进制和/或十六进制值。 

当您需要搜索自定义的原始字节序列时，请使用此选项： 

```bash
$ binwalk -R "\x00\x01\x02\x03\x04" firmware.bin

DECIMAL   	HEX       	DESCRIPTION
-------------------------------------------------------------------------------------------------------------------
377654    	0x5C336   	Raw string signature
```

***

## -A, --opcodes

这指示 binwalk 在指定文件中搜索各种 CPU 架构通用的可执行操作码。  请注意，某些操作码签名很短，因此容易产生误报结果。 

当您需要在文件中定位可执行代码，或者如果您需要确定可执行文件的体系结构时，请使用此选项： 

```bash
$ binwalk -A firmware.bin

DECIMAL         HEX             DESCRIPTION
-------------------------------------------------------------------------------------------------------------------
268             0x10C           MIPS instructions, function prologue
412             0x19C           MIPS instructions, function prologue
636             0x27C           MIPS instructions, function prologue
812             0x32C           MIPS instructions, function epilogue
920             0x398           MIPS instructions, function epilogue
948             0x3B4           MIPS instructions, function prologue
1056            0x420           MIPS instructions, function epilogue
1080            0x438           MIPS instructions, function prologue
1356            0x54C           MIPS instructions, function epilogue
1392            0x570           MIPS instructions, function prologue
1836            0x72C           MIPS instructions, function epilogue
2012            0x7DC           MIPS instructions, function prologue
2260            0x8D4           MIPS instructions, function epilogue
2512            0x9D0           MIPS instructions, function prologue
2552            0x9F8           MIPS instructions, function epilogue
```

***

## -m, --magic=&lt;file&gt;

加载备用魔术签名文件而不是默认文件。 

如果您有一个 [自定义魔术签名文件 ](https://github.com/devttys0/binwalk/wiki/Signature-File-Format/)包含要搜索的签名：

```bash
$ binwalk -m ./foobar.mgc firmware.bin

DECIMAL         HEX             DESCRIPTION
-------------------------------------------------------------------------------------------------------------------
268             0x10C           Foobar
412             0x19C           Foobar
636             0x27C           Foobar
```

***

## -b, --dumb

禁用“智能”签名匹配。 

当误报签名中的智能签名关键字导致其他有效签名被遗漏（例如，通过跳转到偏移关键字）时很有用： 

```bash
$ binwalk -b firmware.bin
```

***

## -I, --invalid

显示所有结果，甚至那些标记为无效的结果。 

如果您认为 binwalk 将有效文件视为无效文件，则很有用，但会产生大量垃圾输出： 

```bash
$ binwalk -I firmware.bin
```

***

## -x, --exclude=&lt;filter&gt;

排除与指定排除过滤器匹配的签名。  过滤器是小写的正则表达式；  可以指定多个过滤器。 

第一行与指定过滤器匹配的魔术签名根本不会被加载；  因此，使用此过滤器可以帮助减少签名扫描时间。 

用于排除不需要或无趣的结果： 

```bash
$ binwalk -x 'mach-o' -x '^hp' firmware.bin # exclude HP calculator and OSX mach-o signatures
```

***

## -y, --include=&lt;filter&gt;

仅包括与指定的包含过滤器匹配的签名。  过滤器是小写的正则表达式；  可以指定多个过滤器。 

只有第一行与指定过滤器匹配的魔术签名才会被加载；  因此，使用此过滤器可以帮助减少签名扫描时间。 

仅搜索特定签名或签名类型时很有用： 

```bash
$ binwalk -y 'filesystem' firmware.bin # only search for filesystem signatures
```

***

## -Y, --disasm

尝试使用 capstone 反汇编程序识别文件中包含的可执行代码的 CPU 架构。 

指定 [--verbose ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#verbose)将另外打印反汇编指令。 

通常比 [--opcodes ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#opcodes)，但支持的架构更少： 

```bash
$ binwalk --disasm firmware.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
428           0x1AC           MIPS executable code, 32/64-bit, little endian, at least 750 valid instructions
```

***

## -T, --minsn

的最小连续指令数设置为 [--disasm ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#disasm)有效。 默认为 500 条指令： 

```bash
$ binwalk --minsn=1200 -Y firmware.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
428           0x1AC           MIPS executable code, 32/64-bit, little endian, at least 1250 valid instructions
```

***

## -k, --continue

指示 [--disasm ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#disasm)不要停留在第一个结果： 

```bash
$ binwalk --continue -Y firmware.bin

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
428           0x1AC           MIPS executable code, 32/64-bit, little endian, at least 1250 valid instructions
1048576       0x100000        MIPS executable code, 32/64-bit, little endian, at least 1250 valid instructions
...
```

***

## -E, --entropy

对输入文件执行熵分析，打印原始熵数据并生成熵图。 

熵分析可以与 [--signature ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#signature)、 [--raw ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#raw)或 [--opcodes ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#opcodes)以更好地理解目标文件。 

用于识别签名扫描可能遗漏的有趣数据部分： 

```bash
$ binwalk -E firmware.bin
DECIMAL       HEXADECIMAL     ENTROPY
--------------------------------------------------------------------------------
0             0x0             Rising entropy edge (0.983751)
1155072       0x11A000        Falling entropy edge (0.000000)
1181696       0x120800        Rising entropy edge (0.990546)
3780608       0x39B000        Falling entropy edge (0.000000)
```

当与 [--verbose ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#verbose)选项结合使用时，会打印为每个数据块计算的原始熵： 

```bash
$ binwalk -E --verbose firmware.bin

DECIMAL         HEX             ENTROPY ANALYSIS
--------------------------------------------------------------------------------
0               0x0             0.964914
1024            0x400           0.978591
2048            0x800           0.973048
3072            0xC00           0.976195
4096            0x1000          0.976072
5120            0x1400          0.976734
6144            0x1800          0.976861
7168            0x1C00          0.972385
8192            0x2000          0.972518
...
```

**PYTHON API 警告：** binwalk ( [pyqtgraph ](http://www.pyqtgraph.org/)) 使用的绘图模块调用 `os._exit`完成后; 这显然是处理各种 QT 问题所必需的。 从命令行运行 binwalk 时，熵分析总是最后完成，几乎不用担心。 但是，如果通过 API 调用熵分析，请务必禁用绘图 ( [--nplot ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#nplot)) 以防止您的脚本过早退出。 

***

## -J, --save

自动将 [--entropy ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#entropy)到 PNG 文件中，而不是显示它。 

```bash
$ binwalk --save -E firmware.bin
```

***

## -Q, --nlegend

生成的熵图中 [--entropy ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#entropy)：

```bash
$ binwalk --entropy -Q firmware.bin
```

***

## -N, --nplot

图形熵图 [--entropy ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#entropy)扫描 ：

```bash
$ binwalk --entropy -N firmware.bin
```

***

## -H, --high=&lt;float&gt;

设置上升沿熵触发电平。 仅在与 [--entropy ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#entropy)。  指定值应介于 0 和 1 之间：

```bash
$ binwalk --entropy -H .9 firmware.bin
```

***

## -L, --low=&lt;float&gt;

设置下降沿熵触发电平。 仅在与 [--entropy ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#entropy)。  指定值应介于 0 和 1 之间： 

```bash
$ binwalk --entropy -L .3 firmware.bin
```

***

## -W, --hexdump

执行输入文件的十六进制转储和颜色代码字节，如下所示： 

<ul>
	<li><a href="#green">Green</a> - 这些字节在所有文件中都相同 </li>
	<li><a href="#red">Red</a>   - 这些字节在所有文件中都不同</li>
	<li><a href="#blue">Blue</a>  - 这些字节仅在某些文件中不同</li>
</ul>



可以区分任意数量的文件； 其他有用的选项是 [--block ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#block)、 [--offset ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#offset)、 [--length ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#length)和 [--terse ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#terse)： 

```bash
$ binwalk -W --block=8 --length=64 firmware1.bin firmware2.bin firmware3.bin
```

注意：如果您需要分页输出，请安装 `most`实用程序，因为它更好地支持彩色输出的分页。 

***

## -G, --green

期间仅显示包含绿色字节的 [--hexdump ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#hexdump)：

```bash
$ binwalk -W --green firmware1.bin firmware2.bin firmware3.bin
```

***

## -i, --red

期间仅显示包含红色字节的 [--hexdump ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#hexdump)： 

```bash
$ binwalk -W --red firmware1.bin firmware2.bin firmware3.bin
```

***

## -U, --blue

期间仅显示包含蓝色字节的 [--hexdump ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#hexdump)： 

```bash
$ binwalk -W --blue firmware1.bin firmware2.bin firmware3.bin
```

***

## -w, --terse

执行 [--hexdump ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#hexdump)时，仅显示第一个文件的十六进制转储。 

在区分许多不适合屏幕的文件时很有用： 

```bash
$ binwalk -W --terse firmware1.bin firmware2.bin firmware3.bin
```

***

## -e, --extract

加载常用 [--dd ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#dd)提取规则， [预定义的文件 ](https://github.com/ReFirmLabs/binwalk/blob/master/src/binwalk/config/extract.conf)并从 `~/.config/binwalk/config/extract.conf`. 

```bash
$ binwalk -e firmware.bin
```

***

## -D, --dd=&lt;type[:ext[:cmd]]&gt;

提取在 [--signature ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#signature)扫描期间识别的文件。 可以指定多个 --dd 选项。 

- **type** 是签名描述中包含的*小写*字符串（支持正则表达式） 
- **ext** 是保存数据盘时使用的文件扩展名（默认无） 
- **cmd** 是数据保存到磁盘后执行的可选命令 

默认情况下，文件名是找到签名的十六进制偏移量，除非在签名本身中指定了备用文件名。 

以下示例演示了使用 --dd 选项指定提取规则，该选项将提取包含字符串 'zip archive' 且文件扩展名为 'zip' 的任何签名，然后执行 'unzip' 命令。  此外，PNG 图像按原样提取，文件扩展名为“png”。 

请注意“%e”占位符的使用。  执行 unzip 命令时，此占位符将替换为解压缩文件的相对路径： 

```bash
$ binwalk -D 'zip archive:zip:unzip %e' -D 'png image:png' firmware.bin
```

***

## -M, --matryoshka

期间递归扫描提取的文件 [--signature ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#signature)。 仅在与 [--extract ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#extract)或 [--dd ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#dd)。 

```bash
$ binwalk -e -M firmware.bin
```

***

## -C, --directory=&lt;str&gt;

设置提取数据的输出目录（默认：当前工作目录）。 

一起使用时适用 [--extract ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#extract)或 [--dd ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#dd)选项 ：

```bash
$ binwalk -e --directory=/tmp firmware.bin
```

***

## -d, --depth=&lt;int&gt;

限制 [--matryoshka ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#matryoshka)递归深度。 默认情况下，深度设置为 8。 

一起使用时适用 [--matryoshka ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#matryoshka)选项 

```bash
$ binwalk -Me -d 5 firmware.bin
```

***

## -j, --size=&lt;int&gt;

限制从目标文件中提取的数据大小。  默认情况下，没有大小限制。 

仅在与 [--extract ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#extract)或 [--dd ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#dd)。 

请注意，此选项不限制外部提取实用程序提取/解压缩的数据大小。 

从磁盘空间有限的大文件中雕刻或提取数据时很有用： 

```bash
$ binwalk -e --size=0x100000 firmware.bin
```

***

## -r, --rm

清理零大小文件和提取实用程序在提取期间无法处理的文件。 

仅在与 [--extract ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#extract)或 [--dd ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#dd)。 

用于清理提取期间从目标文件中复制的误报文件： 

```bash
$ binwalk -e -r firmware.bin
```

***

## -z, --carve

仅执行数据雕刻，不执行外部提取实用程序。 

仅在与 [--extract ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#extract)或 [--dd ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#dd)。 

当您只想从目标文件中提取数据但不自动提取/解压缩该数据时很有用： 

```bash
$ binwalk -e --carve firmware.bin
```

***

## -X, --deflate

通过蛮力识别可能的原始放气压缩数据流。 

对于从带有损坏/修改/丢失标题的文件中恢复数据很有用。 可以与 [--lzma ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#lzma)。 

此扫描可能很慢，因此使用 [--offset ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#offset)和/或 [--length ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#length)： 

```bash
$ binwalk --deflate -o 0x100 -l 10000 firmware.bin
```

***

## -Z, --lzma

通过蛮力识别可能的原始 LZMA 压缩数据流。 

对于从带有损坏/修改/丢失标题的文件中恢复数据很有用。 可以与 [--deflate ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#deflate)。 

由于 LZMA 压缩选项的数量不同，此扫描可能非常慢，因此使用 [--offset ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#offset)和/或 [--length ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#length)： 

```bash
$ binwalk --lzma -o 0x100 -l 10000 firmware.bin
```

***

## -P, --partial

仅使用常用压缩选项搜索压缩流。 可以显着提高 [--lzma ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#lzma)扫描的速度： 

```bash
$ binwalk --partial -Z -o 0x100 -l 10000 firmware.bin
```

***

## -S, --stop

当与 [--lzma ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#lzma)和/或 [--deflate ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#deflate)选项一起使用时，这将在显示第一个结果后停止扫描： 

```bash
$ binwalk --stop -Z firmware.bin
```

***

## -l, --length=&lt;int&gt;

设置要在目标文件中分析的字节数： 

```bash
$ binwalk --length=0x100 firmware.bin
```

***

## -o, --offset=&lt;int&gt;

设置开始分析目标文件的起始偏移量。  也可以指定负偏移量（与文件结尾的距离）： 

```bash
$ binwalk --offset=0x100 firmware.bin
```

***

## -O, --base=&lt;int&gt;

设置所有打印偏移的基地址。 此值将添加到所有打印结果的原始文件偏移量中： 

```bash
$ binwalk --base=0x80001000 firmware.bin
```

***

## -K, --block=&lt;int&gt;

设置分析期间使用的块大小（以字节为单位）。 

当与 [--entropy ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#entropy)，这将确定在熵分析期间分析的每个块的大小。 

当与 [--hexdump ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#hexdump)，这将设置十六进制输出中每行显示的字节数。 

```bash
$ binwalk --diff -K 8 firmware1.bin firmware2.bin
```

***

## -g, --swap=&lt;int&gt;

反转每个 `n`扫描它们之前的字节： 

```bash
$ binwalk --swap=2 firmware.bin
```

***

## -f, --log=&lt;file&gt;

将扫描结果记录到指定文件。 

，否则保存到日志文件的数据将与终端中显示的数据相同 [--csv ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#csv)。 

，数据也会保存到日志文件 [--quiet ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#quiet)中： 

```bash
$ binwalk --log=binwalk.log firmware.bin
```

***

## -c, --csv

使日志数据以 CSV 格式保存。 如果与 [--cast ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#cast)或 [--hexdump ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#hexdump)。 

仅在与 [--log ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#log)选项结合使用时有效： 

```bash
$ binwalk --log=binwalk.log --csv firmware.bin
```

***

## -t, --term

将输出格式化为当前终端窗口宽度。 

有助于使长行换行输出更具可读性： 

```bash
$ binwalk --term firmware.bin

DECIMAL   	HEX       	DESCRIPTION
-------------------------------------------------------------------------------------------------------
0         	0x0       	DLOB firmware header, boot partition: "dev=/dev/mtdblock/2"
112       	0x70      	LZMA compressed data, properties: 0x5D, dictionary size: 33554432
                        bytes, uncompressed size: 3805904 bytes
1310832   	0x140070  	PackImg section delimiter tag, little endian size: 15741184 bytes; big
                        endian size: 3272704 bytes
1310864   	0x140090  	Squashfs filesystem, little endian, version 4.0, compression:lzma,
                        size: 3268870 bytes,  1860 inodes, blocksize: 65536 bytes, created:
                        Mon Apr 22 04:56:42 2013
```

***

## -q, --quiet

禁用输出到标准输出。 

一起使用时最方便 [--log ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#log)或详细扫描（如 [--entropy ） ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#entropy)： 

```bash
$ binwalk --quiet -f binwalk.log firmware.bin
```

***

## -v, --verbose

启用详细输出，包括目标文件 MD5 和扫描时间戳。 

，则将显示来自外部提取实用程序的输出 [--extract ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#extract)： 

```bash
$ binwalk --verbose firmware.bin

Scan Time:     2013-11-10 21:04:04
Signatures:    265
Target File:   firmware.bin
MD5 Checksum:  6b91cdff1b4f0134b24b7041e079dd3e

DECIMAL   	HEX       	DESCRIPTION
-------------------------------------------------------------------------------------------------------------------
0         	0x0       	DLOB firmware header, boot partition: "dev=/dev/mtdblock/2"
112       	0x70      	LZMA compressed data, properties: 0x5D, dictionary size: 33554432 bytes, uncompressed size: 3805904 bytes
1310832   	0x140070  	PackImg section delimiter tag, little endian size: 15741184 bytes; big endian size: 3272704 bytes
1310864   	0x140090  	Squashfs filesystem, little endian, version 4.0, compression:lzma, size: 3268870 bytes,  1860 inodes, blocksize: 65536 bytes, created: Mon Apr 22 04:56:42 2013
```

***

## -h, --help

显示 binwalk 帮助输出： 

```bash
$ binwalk --help
```

***

## -a, --finclude=&lt;str&gt;

仅扫描名称与给定正则表达式字符串匹配的文件。 结合使用时特别有用 [--matryoshka ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#matryoshka)和 [--extract ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#extract)

```bash
$ binwalk -M -e --finclude='\.bin$' firmware.bin
```

***

## -p, --fexclude=&lt;str&gt;

不要扫描名称与给定正则表达式字符串匹配的文件。 结合使用时特别有用 [--matryoshka ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#matryoshka)和 [--extract ](https://github.com/ReFirmLabs/binwalk/wiki/Usage#extract)

```bash
$ binwalk -M -e --fexclude='\.pdf$' firmware_archive.zip
```

***

## -s, --status=&lt;int&gt;

在指定的端口号上启用状态服务器。  状态服务器仅在 localhost 上侦听并打印出与当前扫描状态相关的人类可读的 ASCII 数据。  您可以使用 telnet、netcat 等连接到它。 

```bash
$ binwalk --status=8080 firmware_archive.zip
```

***
