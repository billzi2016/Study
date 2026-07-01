# Window Functions

本目录用于可视化常见窗函数的时域形状和频域幅度响应。图片由 `plot_window_functions.py` 使用 `scipy.signal.windows` 生成，并通过 `matplotlib.pyplot` 保存为 JPG。

窗函数是在截取有限长度信号时乘上的一组权重。实际做 FFT 或设计 FIR 滤波器时，我们经常只能处理有限长度的数据；直接截断等价于乘以矩形窗，会在频域中产生明显的频谱泄漏。窗函数的作用就是控制这种截断带来的影响。

窗函数的核心取舍通常是：

- 主瓣宽度：主瓣越窄，频率分辨率越高，越容易区分相近频率。
- 旁瓣高度：旁瓣越低，频谱泄漏越少，弱信号越不容易被强信号掩盖。
- 衰减速度：旁瓣下降越快，远离主频的泄漏越弱。
- 幅度精度：有些窗更适合测频率，有些窗更适合测幅度。

没有一个窗函数在所有指标上都最好。选择窗函数时，本质是在“频率分辨率”和“泄漏抑制”之间做取舍。

## 图像说明

每张图片包含两个子图：

- Time domain：窗函数在采样点上的权重形状。
- Frequency domain：归一化频率下的幅度响应，单位为 dB。

频域图中，中间最高的部分是主瓣，主瓣两侧较小的波纹是旁瓣。主瓣越窄，频率分辨率越好；旁瓣越低，泄漏越小。

## 窗函数特点

### Boxcar / Rectangular

矩形窗是不做平滑的直接截断，所有采样点权重相同。它的主瓣最窄，频率分辨率高，但旁瓣很高，频谱泄漏严重。适合信号刚好周期完整、或只关心最高分辨率且能接受泄漏的情况。

![boxcar](boxcar.jpg)

### Triangular

三角窗从两端逐渐上升到中间再下降，比矩形窗平滑。它能降低旁瓣，但主瓣会变宽。适合需要比矩形窗更少泄漏、但仍希望保持较简单形状的场景。

![triang](triang.jpg)

### Bartlett

Bartlett 窗也是三角形窗的一种常见定义，端点通常为零。它相比矩形窗能减少频谱泄漏，但频率分辨率下降。适合基础频谱分析教学和简单平滑截断。

![bartlett](bartlett.jpg)

### Hann

Hann 窗两端平滑降到零，频域旁瓣比矩形窗低很多，是频谱分析中很常用的默认选择。它在分辨率和泄漏抑制之间比较均衡。适合一般 FFT 分析、周期不完整信号分析和教学示例。

![hann](hann.jpg)

### Hamming

Hamming 窗与 Hann 类似，但端点不完全为零。它的第一旁瓣通常比 Hann 更低，但远端旁瓣下降速度相对不同。适合语音处理、频谱估计和需要压低近旁瓣的场景。

![hamming](hamming.jpg)

### Blackman

Blackman 窗比 Hann 和 Hamming 有更强的旁瓣抑制，但主瓣更宽。它适合需要更低泄漏、并且可以接受频率分辨率下降的分析任务。

![blackman](blackman.jpg)

### Blackman-Harris

Blackman-Harris 窗具有很低的旁瓣，泄漏抑制能力强，但主瓣较宽。适合检测弱信号、动态范围要求高的频谱分析场景。

![blackmanharris](blackmanharris.jpg)

### Nuttall

Nuttall 窗与 Blackman-Harris 类似，也强调低旁瓣和良好的动态范围。它适合在强弱信号同时存在时减少强信号泄漏对弱信号的干扰。

![nuttall](nuttall.jpg)

### Flat Top

Flat Top 窗的频域顶部更平坦，主要优点是幅度测量准确，缺点是主瓣很宽、频率分辨率较差。适合需要准确测量正弦信号幅值的场景，例如仪器测量和幅度校准。

![flattop](flattop.jpg)

### Parzen

Parzen 窗比较平滑，旁瓣衰减较快，但主瓣较宽。它适合需要平滑过渡和较强远端泄漏抑制的场景。

![parzen](parzen.jpg)

### Bohman

Bohman 窗两端平滑为零，形状由余弦和线性项组合而成。它有较好的旁瓣衰减，适合对截断边缘平滑性有要求的频谱分析。

![bohman](bohman.jpg)

### Cosine

Cosine 窗使用简单的余弦形状，两端较低、中间较高。它比矩形窗平滑，泄漏更少，但抑制能力不如 Blackman-Harris 等低旁瓣窗。适合直观理解平滑窗的基本效果。

![cosine](cosine.jpg)

### Tukey

Tukey 窗也叫 tapered cosine window，可以看作矩形窗和 Hann 窗之间的折中。中间较平，两端用余弦平滑过渡。`alpha` 越小越接近矩形窗，`alpha` 越大越接近 Hann 窗。

![tukey_alpha_0_5](tukey_alpha_0_5.jpg)

### Kaiser

Kaiser 窗通过 `beta` 参数控制主瓣宽度和旁瓣高度。`beta` 越大，旁瓣越低，但主瓣越宽。它的灵活性很高，常用于 FIR 滤波器设计。

![kaiser_beta_14](kaiser_beta_14.jpg)

### Gaussian

Gaussian 窗使用高斯曲线作为权重，时域和频域都比较平滑。`std` 控制宽度，标准差越大，窗越宽。它适合需要平滑局部加权的时频分析场景。

![gaussian_std_40](gaussian_std_40.jpg)

### General Gaussian

General Gaussian 窗是 Gaussian 窗的推广，通过 `p` 和 `sig` 控制曲线形状。它可以在更尖锐或更平缓的形状之间调整，适合比较不同平滑程度对频谱的影响。

![general_gaussian_p_1_5_sig_40](general_gaussian_p_1_5_sig_40.jpg)

### Chebyshev

Chebyshev 窗可以指定旁瓣衰减量，旁瓣通常呈等波纹特征。它适合明确要求某个旁瓣抑制指标的场景，常用于滤波器和阵列信号处理。

![chebwin_at_100](chebwin_at_100.jpg)

### Exponential

Exponential 窗按指数规律衰减，常用于强调某一侧或中心附近样本的权重。`tau` 控制衰减速度。它适合模拟阻尼、衰减过程或需要指数加权的分析。

![exponential_tau_40](exponential_tau_40.jpg)

### Taylor

Taylor 窗常用于天线阵列和雷达相关应用，可以控制近旁瓣水平，同时保持相对可控的主瓣宽度。它适合对旁瓣形状有工程指标要求的场景。

![taylor](taylor.jpg)

### Lanczos

Lanczos 窗基于 sinc 形状，常见于插值、重采样和信号重建相关问题。它在保留中心信息和抑制截断振铃之间做折中。

![lanczos](lanczos.jpg)

## 重新生成图片

如果需要重新生成所有 JPG，可以在仓库根目录运行：

```bash
python3 window_functions/plot_window_functions.py
```

脚本会覆盖同名 JPG 图片。
