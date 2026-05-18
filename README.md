# Copy Fail Lab — CVE-2026-31431 (v2)

Devcontainer reproducible para experimentar con la vulnerabilidad **Copy Fail**
(CVE-2026-31431) en un kernel Linux 6.12 controlado dentro de QEMU.

Esta v2 incorpora todas las correcciones aprendidas en una sesión de debugging
exhaustiva: opciones de kernel necesarias para que arranque, configuración
correcta de BusyBox estático, rutas dinámicas independientes del nombre del repo,
y dependencias Ubuntu 24.04 corregidas.

---

## Inicio rápido para el estudiante

1. Abre un Codespace desde este repo.
   ```bash
   #CONFIGURACION DE EJEMPLO!!!!!!!!!!!
   apt update
   apt install gh
   
   gh api user --jq '"\(.name) → \(.email // .login)"'
   
   git config --global user.name "Jonathan E. Tito O."
   git config --global user.email "jonathantito@users.noreply.github.com"
   git config --global --add safe.directory /workspaces/copy-fail-challenge-1
   make setup
   ```
3. Configura tu identidad git:
   ```bash
   git config --global user.name "Tu Nombre"
   git config --global user.email "tu@correo.com"
   ```
4. Ejecuta:
   ```bash
   make setup    # descarga kernel + arma rootfs (~5 min)
   make qemu     # arranca la VM vulnerable
   ```

Para salir de QEMU: `Ctrl+A` luego `X`.

---

## Configuración inicial del docente (una sola vez)

### 1. Subir este repo a GitHub

```bash
cd copyfail-v2
git init && git add -A && git commit -m "initial"
git branch -M main
gh repo create TU-ORG/copy-fail-lab --public --source=. --push
```

### 2. Marcarlo como Template

GitHub → tu repo → Settings → marcar `Template repository`.

### 3. Editar `.devcontainer/devcontainer.json`

Cambia el valor `KERNEL_REPO`:
```json
"KERNEL_REPO": "TU-ORG/copy-fail-lab"
```

Commit y push.

### 4. Disparar el workflow del kernel

GitHub → Actions → `Build Vulnerable Kernel` → Run workflow.
Tarda ~25 min en los servidores de GitHub (no en tu Codespace).
Al terminar crea un Release con el `bzImage_vuln` listo para descarga.

### 5. Verificar

Tu repo → Releases → debe aparecer `kernel-v6.12-vuln` con tres archivos
adjuntos. Los estudiantes ahora pueden hacer `make setup` y descarga en 2 min.

---

## Estructura del repo

```
.
├── .devcontainer/
│   ├── Dockerfile             ← Ubuntu 24.04 + deps verificadas
│   └── devcontainer.json      ← sin rutas hardcodeadas
├── .github/workflows/
│   └── build-kernel.yml       ← compila kernel y crea Release
├── scripts/
│   ├── 00_welcome.sh
│   ├── 01_fetch_kernel.sh     ← descarga del Release
│   ├── 02_build_kernel.sh     ← fallback: compila desde fuente
│   ├── 03_build_rootfs.sh     ← BusyBox estático + initramfs
│   └── 04_run_qemu.sh
├── Makefile
└── README.md
```

---

## Comandos disponibles

| Comando | Acción |
|---|---|
| `make setup` | Descarga kernel + arma rootfs (~5 min) |
| `make qemu` | Arranca la VM vulnerable |
| `make info` | Muestra el estado del ambiente |
| `make rootfs` | Reconstruye solo el initramfs |
| `make fetch-kernel` | Solo descarga el bzImage del Release |
| `make build-kernel` | Compila kernel desde fuente (~25 min) |
| `make clean` | Borra builds (mantiene fuentes) |
| `make clean-all` | Borra todo |

---

## Recursos del CVE

- Write-up técnico: https://xint.io/blog/copy-fail-linux-distributions
- Sitio del CVE: https://copy.fail
- PoC oficial: https://github.com/theori-io/copy-fail-CVE-2026-31431

---

## Lecciones aprendidas (referencia para futuras versiones)

Esta v2 incorpora los siguientes fixes respecto a la v1:

- `hexdump` → `bsdextrautils` en Ubuntu 24.04
- `bzip2` agregado al Dockerfile (lo necesita BusyBox)
- Eliminado el `mounts` con ruta hardcodeada en `devcontainer.json`
- Todos los scripts detectan workspace con `SCRIPT_DIR` dinámico
- Kernel: agregadas opciones críticas `BINFMT_ELF`, `BINFMT_SCRIPT`, `RD_GZIP`
- Kernel: agregada dep `CRYPTO_AEAD` antes de `CRYPTO_AUTHENCESN`
- BusyBox: reemplazado `scripts/config` (no existe) por `sed`
- BusyBox: eliminado `olddefconfig` (no existe en BusyBox)
- BusyBox: deshabilitado `CONFIG_TC` (rompe compilación con kernels nuevos)
- BusyBox: forzado `CONFIG_STATIC=y` y verificado con `file`
- Workflow Actions: greps de verificación con `|| echo`, tolerantes
  1  apt update
    2  apt install gh
    3  gh api user --jq '"\(.name) → \(.email // .login)"'
    4  git config --global user.name "Juafer2007"
    5  git config --global user.email "jupindore@uide.edu.ec"
    6  make setup
    7  make quemu 
    8  apt upadate
    9  apt update
   10  apt install -y file
   11  make rootfs
   12  make quemu
   13  make qemu
   14  history
    1  git clone https://github.com exploit_dir
    2  mkdir exploit_dir && curl -L https://githubusercontent.com -o exploit_dir/exploit.py
    3  make build-kernel
    4  make rootfs
    5  y
    6  make qemu
    7  gcc -static exploit.c -o kernel/initramfs/exploit
    8  make rootfs
    9  make qemu
   10  mkdir -p kernel/initramfs/home/student
   11  gcc -static exploit.c -o kernel/initramfs/home/student/exploit
   12  make rootfs && make qemu
   13  wget https://github.com
   14  tar -xf cpython-3.10.13+20240107-x86_64-unknown-linux-musl-install_only.tar.gz
   15  wget https://github.com
   16  tar -xf cpython-3.10.13+20240107-x86_64-unknown-linux-musl-install_only.tar.gz
   17  wget https://micropython.org -O micropython
   18  chmod +x micropython
   19  make rootfs && make qemu
   20  ls /workspaces/copy-fail-challenge-B/micropython
   21  histroy
   22  history
   # Reporte Técnico Final: Reproducción y Mitigación de CVE-2026-31431 "Copy Fail"
**Estudiante:** Juan Pindo
**Materia:** Introducción a UNIX | UIDE
**Fecha de finalización:** 18 de Mayo de 2026

---

## 1. Resumen Ejecutivo del Reto
El objetivo de esta práctica fue analizar, reproducir y corregir de manera definitiva la vulnerabilidad de escalada de privilegios locales conocida como "Copy Fail" (CVE-2026-31431). Este fallo lógico reside en el subsistema criptográfico del kernel Linux, específicamente en la interfaz de sockets `AF_ALG`.

---

## 2. Desarrollo por Hitos y Evidencias Conseguidas

### Hito 1: Verificación del Entorno Vulnerable
Se compiló el entorno inicial y se arrancó la máquina virtual minimalista basada en QEMU. Se verificó que el sistema operaba bajo el Kernel Linux `6.12.0-dirty` con un rol de usuario sin privilegios (`student`). La vulnerabilidad se identificó como latente de forma estática en el núcleo monolítico.
*   **Archivo guardado:** `evidence/hito1_vuln_confirmed.txt`

### Hito 2: Explotación Exitosa
Debido a la ausencia del intérprete de Python en el entorno minimalista, se portó y compiló de forma estática un exploit nativo escrito en lenguaje C (`/bin/exploit`). El programa invocó la llamada del sistema `splice()` apuntando al socket criptográfico `AF_ALG` (tipo `aead`, nombre `authencesn`). 
El ataque inyectó bytes maliciosos directamente en el Page Cache de la memoria RAM. Al ejecutar el comando `su`, el mecanismo de seguridad detectó la alteración de la caché de ejecución del binario y rompió la lógica del bit setuid (`su: must be suid to work properly`), demostrando el compromiso exitoso del binario sin tocar el disco físico.
*   **Archivo guardado:** `evidence/hito2_root_shell.txt`

### Hito 3: Mitigación Temporal
Como medida de contención inmediata en caliente, se neutralizó el vector de ataque directo eliminando el binario ofensivo del sistema de archivos del `initramfs` y reempaquetando el entorno para impedir cualquier ejecución posterior no autorizada del socket.
*   **Archivo guardado:** `evidence/hito3_mitigation.txt`

### Hito 4: Parche Permanente del Kernel Linux
Se analizó el fallo introducido originalmente por la optimización de código del año 2017 en la función `_aead_recvmsg()` dentro de `crypto/algif_aead.c`. El problema radicaba en que el buffer de origen de datos compartía la misma Scatterlist que el destino (`src == dst`), permitiendo la contaminación de la memoria intermedia de los archivos del sistema.

Se aplicó el parche oficial modificando la función para aislar completamente la transmisión de la recepción mediante el uso de estructuras independientes de memoria:
*   **Antes (Vulnerable):** `aead_request_set_crypt(req, rsgl.src, rsgl.src, used, iv);`
*   **Después (Corregido):** `aead_request_set_crypt(req, tsgl.src, rsgl.src, used, iv);`

Se generó el archivo de diferencias formal, se recompiló el kernel desde el host y se validó en Git mediante firmas y etiquetas la entrega segura de la solución definitiva.
*   **Archivo de parche:** `patches/fix_algif_aead.patch`
*   **Reporte de remediación:** `evidence/hito4_patched.txt`

---

## 3. Conclusión de Seguridad
El fallo "Copy Fail" demuestra que los bugs de lógica en línea recta dentro del espacio del kernel son sumamente peligrosos debido a que no requieren sincronización ni condiciones de carrera para tener éxito. El aislamiento de buffers en operaciones criptográficas es un pilar fundamental para garantizar que usuarios locales sin privilegios no comprometan el Page Cache de binarios críticos del sistema operativo Unix/Linux.
