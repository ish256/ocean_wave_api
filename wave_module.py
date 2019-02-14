# gonna put the waves and their models here
import numpy as np


def phillipsSpectrum(waveFieldKx, waveFieldKy, windDirectionNormVect, windSpeed):

    gravityConst = 9.81
    normWaveField = np.sqrt(waveFieldKx**2 + waveFieldKy**2)
    L = (windSpeed**2) / gravityConst
    alpha = 1

    dirSpectrum = (
        waveFieldKx*windDirectionNormVect[0] + waveFieldKy*windDirectionNormVect[1])/normWaveField
    spectrum = alpha * np.exp(-1/(normWaveField*L)**2) * \
        np.abs(dirSpectrum) * (1/normWaveField)**4

    #rmInds = normWaveField == 0
    #spectrum[rmInds] = 0
    spectrum[np.logical_or(dirSpectrum < 0, normWaveField == 0)] = 0

    return spectrum, normWaveField


def initWaveSpectrum(spectrum):

    m, n = spectrum.shape
    randDraw1 = np.random.randn(m, n)
    randDraw2 = np.random.randn(m, n)

    initSpectrum = (1/np.sqrt(2))*(randDraw1 + 1j*randDraw2)*np.sqrt(spectrum)

    return initSpectrum


def makeWaveFieldAtTimeT(initSpectrum, normWaveField, waveFieldDelta, time):

    m, n = initSpectrum.shape
    gravityConst = 9.81
    dispersion = np.sqrt(gravityConst*normWaveField)
    spectralWaveFieldAtT = initSpectrum * \
        np.exp(1j*dispersion*time) + np.transpose(initSpectrum) * \
        np.exp(-1j*dispersion*time)

    # smoothing
    x, y = np.meshgrid(np.arange(m)+1, np.arange(m)+1)
    sgn = np.ones([m, m])
    sgn[np.mod(x+y, 2) == 0] = -1

    waveField = np.fft.ifft2(spectralWaveFieldAtT) * sgn * \
        (m * n * waveFieldDelta * waveFieldDelta)

    return waveField
