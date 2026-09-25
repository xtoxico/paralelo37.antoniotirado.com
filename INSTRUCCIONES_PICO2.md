# Guía de Compilación de Pico FIDO2 para Raspberry Pi Pico 2 (RP2350)

Esta guía detalla los comandos y pasos necesarios para clonar recursivamente el repositorio [librekeys/pico-fido2](https://github.com/librekeys/pico-fido2), instalar las dependencias del sistema y del SDK, y compilar el firmware para la placa **Raspberry Pi Pico 2** (microcontrolador RP2350).

---

## 1. Instalación de Dependencias del Sistema

Para compilar el proyecto se requiere el compilador cruzado para ARM (`arm-none-eabi-gcc`), la librería estándar `newlib`, `cmake`, herramientas de compilación (`make`/`gcc`), `python3`, `git` y la CLI de GitHub (`gh`).

### Arch Linux (Sistema actual)
```bash
sudo pacman -Syu --needed git github-cli cmake base-devel arm-none-eabi-gcc arm-none-eabi-newlib python
```

### Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y git gh cmake build-essential gcc-arm-none-eabi libnewlib-arm-none-eabi libstdc++-arm-none-eabi-newlib python3
```

### Fedora
```bash
sudo dnf install -y git gh cmake make gcc gcc-c++ arm-none-eabi-gcc-cs arm-none-eabi-newlib python3
```

---

## 2. Instalación y Configuración del Raspberry Pi Pico SDK

> [!IMPORTANT]
> La **Raspberry Pi Pico 2** está basada en el procesador **RP2350**. Este microcontrolador **requiere obligatoriamente el Pico SDK v2.0 o superior** (por ejemplo, la versión `2.1.1`). Las versiones 1.5.x no soportan RP2350.

Clona el SDK oficial de Raspberry Pi e inicializa sus submódulos (necesarios para librerías como TinyUSB):

```bash
# 1. Clonar el repositorio del Pico SDK
git clone https://github.com/raspberrypi/pico-sdk.git ~/pico-sdk

# 2. Entrar y cambiar a una versión compatible (v2.1.1 recomendada)
cd ~/pico-sdk
git checkout tags/2.1.1
git submodule update --init

# 3. Exportar la variable de entorno PICO_SDK_PATH
export PICO_SDK_PATH="$HOME/pico-sdk"
```

Para que esta variable se mantenga disponible en futuras sesiones de terminal, añádela a tu archivo de configuración de shell (`~/.bashrc` o `~/.zshrc`):

```bash
echo 'export PICO_SDK_PATH="$HOME/pico-sdk"' >> ~/.bashrc
```

---

## 3. Clonación Recursiva del Repositorio `pico-fido2`

El proyecto `pico-fido2` contiene submódulos anidados esenciales (`pico-fido`, `pico-openpgp`, `pico-keys-sdk`, y dentro de este último `mbedtls`, `tinycbor`, `mlkem`). Por lo tanto, la clonación debe ser **recursiva**.

### Opción A: Usando GitHub CLI (`gh repo clone`)
Puedes pasar argumentos adicionales de git a `gh` usando `--`:

```bash
gh repo clone librekeys/pico-fido2 -- --recurse-submodules
cd pico-fido2
```

### Opción B: Si ya se clonó sin submódulos o vía git estándar
Si ya tienes el repositorio clonado o prefieres inicializar los submódulos manualmente:

```bash
cd pico-fido2
git submodule update --init --recursive
```

---

## 4. Configuración y Compilación para Raspberry Pi Pico 2

Para la **Raspberry Pi Pico 2**:
- Variable de placa: `-DPICO_BOARD=pico2`
- Plataforma RP2350 (ARM Cortex-M33 Secure): `-DPICO_PLATFORM=rp2350-arm-s` *(configurada automáticamente por la placa `pico2` o especificada explícitamente)*.

### Comandos de Compilación

```bash
# 1. Asegurarse de estar en la raíz de pico-fido2
cd pico-fido2

# 2. Asegurarse de que PICO_SDK_PATH está definido
export PICO_SDK_PATH="${PICO_SDK_PATH:-$HOME/pico-sdk}"

# 3. Crear y entrar en el directorio de compilación
mkdir -p build
cd build

# 4. Configurar el proyecto con CMake para Raspberry Pi Pico 2
cmake .. -DPICO_BOARD=pico2 -DPICO_PLATFORM=rp2350-arm-s

# 5. Compilar utilizando todos los núcleos del procesador
make -j$(nproc)
```

Al finalizar la compilación, se generará el archivo binario:
```
build/pico_fido2.uf2
```

---

## 5. Opciones Avanzadas de Compilación (Opcional)

Puedes personalizar las características del firmware pasando banderas a `cmake`:

| Parámetro CMake | Valor por defecto | Descripción |
|---|---|---|
| `-DPICO_BOARD=pico2` | *Requerido* | Define la placa Raspberry Pi Pico 2 |
| `-DPICO_PLATFORM=rp2350-arm-s` | `rp2350-arm-s` | Arquitectura ARM Cortex-M33 para RP2350 |
| `-DENABLE_OATH_APP=ON/OFF` | `ON` | Habilita/deshabilita la app OATH (TOTP / HOTP) |
| `-DENABLE_OTP_APP=ON/OFF` | `ON` | Habilita/deshabilita la emulación de teclado OTP |
| `-DENABLE_PQC=ON/OFF` | `OFF` | Habilita criptografía post-cuántica (ML-KEM) |
| `-DUSB_VID=0xXXXX` | `0x1D50` | Identificador de proveedor USB (Vendor ID) |
| `-DUSB_PID=0xXXXX` | `0x619B` | Identificador de producto USB (Product ID) |

Ejemplo con soporte PQC (ML-KEM):
```bash
cmake .. -DPICO_BOARD=pico2 -DPICO_PLATFORM=rp2350-arm-s -DENABLE_PQC=ON
make -j$(nproc)
```

---

## 6. Flasheo del Firmware en la Raspberry Pi Pico 2

1. **Desconecta** la Raspberry Pi Pico 2 de cualquier puerto USB.
2. Mantén presionado el botón **BOOTSEL** en la placa.
3. Conecta el cable USB al PC mientras mantienes presionado el botón **BOOTSEL**.
4. Suelta el botón **BOOTSEL**. El sistema montará una unidad USB con el nombre `RP2350` (o `RPI-RP2`).
5. Copia el archivo generado `pico_fido2.uf2` a esa unidad USB:
   ```bash
   cp build/pico_fido2.uf2 /run/media/$USER/RP2350/  # (o arrastra el archivo con tu gestor de archivos)
   ```
6. La placa se reiniciará automáticamente y comenzará a operar como llave de seguridad hardware **FIDO2 / WebAuthn / OpenPGP**.

---

## 7. Solución de Problemas Frecuentes

- **Error: `PICO_SDK_PATH not found` o submódulos de pico-sdk faltantes:**
  Verifica que `echo $PICO_SDK_PATH` apunte al directorio correcto y que hayas ejecutado `git submodule update --init` dentro de `pico-sdk`.
- **Error: `fatal error: mbedtls/config.h: No such file or directory`:**
  Los submódulos anidados no fueron descargados. Ejecuta en la raíz de `pico-fido2`:
  ```bash
  git submodule update --init --recursive
  ```
- **Error con `arm-none-eabi-gcc` no encontrado:**
  Verifica la instalación de la toolchain con:
  ```bash
  arm-none-eabi-gcc --version
  ```
