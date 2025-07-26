# Funcion para estandarizar el ploteo de parametros S así quedan todos iguales

import matplotlib.pyplot as plt
import numpy as np

def plot_s_parameters(network, title='Análisis de Parámetros S', save_fig=False, autoscales=False):
    # Configuración del estilo
    plt.style.use('seaborn-v0_8-darkgrid')
    plt.rcParams['figure.figsize'] = (18, 5)
    plt.rcParams['font.size'] = 12

    # Crear figura con 3 subplots horizontales
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle(title, fontsize=16, y=1.05)

    # -----------------------------------------------------------------------------
    # Gráfico 1: Transferencias (S21 y S31) - Escala: -3.4 dB a -2.9 dB
    # -----------------------------------------------------------------------------
    ax1.set_title('Transferencias', fontweight='bold')
    ax1.plot(network.frequency.f/1e9, 20*np.log10(np.abs(network.s[:, 1, 0])), label='$S_{21}$', linewidth=2, color='royalblue')
    ax1.plot(network.frequency.f/1e9, 20*np.log10(np.abs(network.s[:, 2, 0])), label='$S_{31}$', linewidth=2, color='darkorange')
    ax1.axvline(1.0, color='blue', linewidth=1)  # Línea vertical en 1 GHz

    # Obtener los índices de los picos máximos
    idx_max_s21 = np.argmax(20 * np.log10(np.abs(network.s[:, 1, 0])))
    idx_max_s31 = np.argmax(20 * np.log10(np.abs(network.s[:, 2, 0])))
    freq_s21 = network.frequency.f[idx_max_s21] / 1e9
    freq_s31 = network.frequency.f[idx_max_s31] / 1e9
    # Añadir líneas verticales en los picos
    ax1.axvline(freq_s21, color='royalblue', linestyle='--', linewidth=1, alpha=0.7, label=f'{freq_s21:.2f}GHz')
    ax1.axvline(freq_s31, color='darkorange', linestyle='--', linewidth=1, alpha=0.7, label=f'{freq_s31:.2f}GHz')

    ax1.set_xlabel('Frecuencia (GHz)')
    ax1.set_ylabel('Magnitud (dB)')
    ax1.legend()
    ax1.grid(True, alpha=0.8)
    if not autoscales:
        ax1.set_ylim(-3.4, -2.9)  # Escala ajustada
    ax1.set_xlim(0.5, 1.5)    # Frecuencia fija

    # -----------------------------------------------------------------------------
    # Gráfico 2: Adaptaciones (S11, S22, S33) - Escala: -15 dB a -35 dB
    # -----------------------------------------------------------------------------
    ax2.set_title('Adaptaciones', fontweight='bold')
    ax2.plot(network.frequency.f/1e9, 20*np.log10(np.abs(network.s[:, 0, 0])), label='$S_{11}$', linewidth=2, color='firebrick')
    ax2.plot(network.frequency.f/1e9, 20*np.log10(np.abs(network.s[:, 1, 1])), label='$S_{22}$', linewidth=2, color='forestgreen')
    ax2.plot(network.frequency.f/1e9, 20*np.log10(np.abs(network.s[:, 2, 2])), label='$S_{33}$', linewidth=2, color='darkviolet')
    ax2.axvline(1.0, color='blue', linewidth=1)  # Línea vertical en 1 GHz

    # Obtener los índices de los mínimos
    idx_min_s11 = np.argmin(20 * np.log10(np.abs(network.s[:, 0, 0])))
    idx_min_s22 = np.argmin(20 * np.log10(np.abs(network.s[:, 1, 1])))
    idx_min_s33 = np.argmin(20 * np.log10(np.abs(network.s[:, 2, 2])))
    freq_s11 = network.frequency.f[idx_min_s11] / 1e9
    freq_s22 = network.frequency.f[idx_min_s22] / 1e9
    freq_s33 = network.frequency.f[idx_min_s33] / 1e9
    # Añadir líneas verticales en los mínimos

    ax2.axvline(freq_s11, color='firebrick', linestyle='--', linewidth=1, alpha=0.7, label=f'{freq_s11:.2f}')
    ax2.axvline(freq_s22, color='forestgreen', linestyle='--', linewidth=1, alpha=0.7, label=f'{freq_s22:.2f}')
    ax2.axvline(freq_s33, color='darkviolet', linestyle='--', linewidth=1, alpha=0.7, label=f'{freq_s33:.2f}')

    ax2.set_xlabel('Frecuencia (GHz)')
    ax2.legend()
    ax2.grid(True, alpha = 0.8)
    if not autoscales:
        ax2.set_ylim(-35, -15)  # Escala ajustada (invertida para mejor visualización)
    ax2.set_xlim(0.5, 1.5)  # Frecuencia fija

    # -----------------------------------------------------------------------------
    # Gráfico 3: Aislación (S23) - Escala: -45 dB a 5 dB
    # -----------------------------------------------------------------------------
    ax3.set_title('Aislación ($S_{23}$)', fontweight='bold')
    ax3.plot(network.frequency.f/1e9, 20*np.log10(np.abs(network.s[:, 2, 1])),
             color='purple', linewidth=2, label='$S_{23}$')
    ax3.axvline(1.0, color='blue', linewidth=1)  # Línea vertical en 1 GHz

    # Obtener el índice del mínimo
    idx_min_s23 = np.argmin(20 * np.log10(np.abs(network.s[:, 2, 1])))
    freq_min_s23 = network.frequency.f[idx_min_s23] / 1e9
      # Añadir línea vertical en el mínimo
    ax3.axvline(freq_min_s23, color='purple', linestyle='--', linewidth=1, alpha=0.7, label=f'{freq_min_s23:.2f}')

    ax3.set_xlabel('Frecuencia (GHz)')
    ax3.legend()
    ax3.grid(True, alpha = 0.8)
    if not autoscales:
        ax3.set_ylim(-45, 5)    # Escala ajustada
    ax3.set_xlim(0.5, 1.5)  # Frecuencia fija

    # Ajustar espaciado y guardar
    plt.tight_layout()
    if save_fig:
        plt.savefig(f'{title}.png', dpi=300, bbox_inches='tight')
    plt.show()
