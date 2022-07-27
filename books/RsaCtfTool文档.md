# RsaCtfTool

RSA多重攻击工具：从弱公钥中解密数据并尝试恢复私钥 自动选择给定公钥的最佳攻击

攻击：

- 弱公钥因式分解
- 维也纳的进攻
- 哈斯塔德的攻击（小公众指数攻击）
- 小 q （q < 100，000）
- 密文和模数攻击之间的共同因素
- 接近 p 和 q 的费马因式分解
- 噱头素数方法
- 过去的CTF素数方法
- 形式为 b^x 的非 RSA 键，其中 b 是素数
- 使用亚富的自初始化二次筛 （SIQS） （https://github.com/DarkenCode/yafu.git)
- 跨多个键的常见因素攻击
- p/q接近小分数时的小分数法
- 当私有指数 d 与模量相比太小时，Boneh Durfee 方法（即 d < n^0.292）
- 椭圆曲线法
- 波拉德 p-1 表示相对平滑的数字
- 梅森素数因式分解
- Factordb
- 隆达尔
- 新奇素数
- 部分 q
- Primefac
- 启城
- 相同的 n，巨大的 e
- 二元多项式分解
- 欧拉法
- 波拉德·罗
- 沃尔夫勒姆·阿尔法
- 厘米因子
- z3 定理证明
- Primorial pm1 gcd
- 梅森 pm1 gcd
- 费马数 gcd
- 斐波那契
- 系统素数 gcd
- 小 crt 指数
- 香克斯的平方形式因式分解 （SQUFOF）
- 铜匠攻击（ROCA）与NECA变体的回归
- 狄克逊
- 布伦特（波拉德罗变体）
- 皮萨诺时期
- NSIF 漏洞、电源模块化因式分解、近功率因数

## 用法

```
usage: RsaCtfTool.py [-h] [--publickey PUBLICKEY] [--timeout TIMEOUT]
                     [--createpub] [--dumpkey] [--ext] [--sendtofdb]
                     [--uncipherfile UNCIPHERFILE] [--uncipher UNCIPHER]
                     [--verbosity {CRITICAL,ERROR,WARNING,DEBUG,INFO}]
                     [--private] [--ecmdigits ECMDIGITS] [-n N] [-p P] [-q Q]
                     [-e E] [--key KEY] [--isconspicuous] [--convert_idrsa_pub] [--isroca] [--check_publickey]
                     [--attack {brent,fermat_numbers_gcd,comfact_cn,wiener,factordb,smallq,pollard_rho,euler,z3_solver,neca,cm_factor,mersenne_pm1_gcd,SQUFOF,small_crt_exp,fibonacci_gcd,smallfraction,boneh_durfee,roca,fermat,londahl,mersenne_primes,partial_q,siqs,noveltyprimes,binary_polinomial_factoring,primorial_pm1_gcd,pollard_p_1,ecm2,cube_root,system_primes_gcd,dixon,ecm,pastctfprimes,qicheng,wolframalpha,hastads,same_n_huge_e,commonfactors,pisano_period,nsif,all}]
```

模式 1：攻击 RSA（指定 --公钥或 n 和 e）

- 公钥：要破解的公共 rsa 密钥。您可以使用通配符导入多个公钥。
- 解密：要解密的密码消息
- 私有：如果恢复，则显示私有 rsa 密钥

模式2：创建给定n和e的公钥文件（指定--createpub）

- n ： 模量
- e ： 公共指数

模式 3：从 PEM/DER 格式的公钥或私钥（指定 --dumpkey）转储公共和/或私有号码（可选，包括扩展模式下的 CRT 参数）

- 密钥：PEM 或 DER 格式的公钥或私钥

### 非密码文件

```
./RsaCtfTool.py --publickey ./key.pub --uncipherfile ./ciphered\_file
```

### 打印私钥

```
./RsaCtfTool.py --publickey ./key.pub --private
```

### 尝试使用常见因素攻击破坏多个公钥，或单独使用通配符两边的引号来阻止 bash 扩展

```
./RsaCtfTool.py --publickey "*.pub" --private
```

### （可选）将结果发送回因子数据库

```
./RsaCtfTool.py --publickey "*.pub" --private --sendtofdb
```

### 生成公钥

```
./RsaCtfTool.py --createpub -n 7828374823761928712873129873981723...12837182 -e 65537
```

### 从键转储参数

```
./RsaCtfTool.py --dumpkey --key ./key.pub
```

### 检查给定的私钥是否显眼

```
./RsaCtfTool.py --key examples/conspicuous.priv --isconspicuous
```

### 当您知道素数的近似长度（以数字为单位）时，使用 ECM 进行因子分解

```
./RsaCtfTool.py --publickey key.pub --ecmdigits 25 --verbose --private
```

有关更多示例，请查看 test.sh 文件

### 将 idrsa.pub 转换为 pem 格式

```
./RsaCtfTool.py --convert_idrsa_pub --publickey $HOME/.ssh/id_rsa.pub
```

### 检查给定的密钥或密钥是否是 roca

```
./RsaCtfTool.py --isroca --publickey "examples/*.pub"
```

### Docker run

```
docker pull ganapati/rsactftool` `docker run -it --rm -v $PWD:/data ganapati/rsactftool <arguments>
```

## 要求

- GMPY2
- SymPy
- PyCrypto
- 请求
- 利布纳姆
- 贤者：可选但可取
- 鼠尾草二进制文件

### Ubuntu 18.04 和 Kali 特定说明

```
git clone https://github.com/Ganapati/RsaCtfTool.git
sudo apt-get install libgmp3-dev libmpc-dev
cd RsaCtfTool
pip3 install -r "requirements.txt"
python3 RsaCtfTool.py
```

### Fedora（33 及以上）具体说明

```
git clone https://github.com/Ganapati/RsaCtfTool.git
sudo dnf install gcc python3-devel python3-pip python3-wheel gmp-devel mpfr-devel libmpc-devel
cd RsaCtfTool
pip3 install -r "requirements.txt"
python3 RsaCtfTool.py
```

如果你也想要可选的SageMath，你需要做

```
sudo dnf install sagemath
pip3 install -r "optional-requirements.txt"
```

### 特定于 MacOS 的说明

如果无法安装环境中可访问的要求，则以下命令可能有效。`pip3 install -r "requirements.txt"`

`easy_install `cat requirements.txt``

### 可选配roca密钥，最高512位，安装neca：

您可以按照以下说明进行操作：`https://www.mersenneforum.org/showthread.php?t=23087`

## 待办事项（又名。需要帮助！

- 请阅读 CONTRIBUTING.md 指南，了解最低限度的可接受 PR。
- 在每次攻击中实施测试方法。
- 以 **Big O** 表示法为每次攻击分配正确的算法复杂性。