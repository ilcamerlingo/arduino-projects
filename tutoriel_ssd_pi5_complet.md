# Tutoriel SSD Pi5 - Installation Complète

## Prérequis

| Matériel | Description |
|----------|-------------|
| **Raspberry Pi 5** | Avec SD card actuelle (OpenClaw) |
| **SSD NVMe** | M.2 NVMe (format 2230, 2242, 2260 ou 2280) |
| **Boîtier NVMe pour Pi5** | HAT NVMe officiel ou compatible |
| **Clavier/Souris** | USB ou Bluetooth |
| **Écran** | HDMI |
| **Alimentation** | USB-C 27W minimum (Pi5 officiel recommandé) |

---

## ÉTAPE 1 : Sauvegarde Complète (AVANT tout arrêt)

### 1.1 Sauvegarde OpenClaw (SUR SUPPORT EXTERNE)

```bash
# Se connecter au Pi (SSH ou direct)
ssh ilcamerlingo@192.168.68.60

# Créer dossier backup
mkdir -p ~/backup_ssd_$(date +%Y%m%d)

# Sauvegarder config OpenClaw
cp -r ~/.openclaw ~/backup_ssd_$(date +%Y%m%d)/

# Sauvegarder scripts personnels
cp -r ~/scripts ~/backup_ssd_$(date +%Y%m%d)/ 2>/dev/null || echo "Pas de dossier scripts"

# Sauvegarder crontab
crontab -l > ~/backup_ssd_$(date +%Y%m%d)/crontab_backup.txt

# Liste des packages installés
pip list > ~/backup_ssd_$(date +%Y%m%d)/pip_packages.txt
dpkg -l > ~/backup_ssd_$(date +%Y%m%d)/apt_packages.txt

# Créer archive
cd ~
tar -czf backup_ssd_$(date +%Y%m%d).tar.gz backup_ssd_$(date +%Y%m%d)/

# IMPORTANT: Copier sur support EXTERNE (clé USB ou Mac)
# Option 1: Clé USB
sudo mkdir -p /mnt/usb
sudo mount /dev/sda1 /mnt/usb  # Adapter selon ta clé
cp backup_ssd_*.tar.gz /mnt/usb/
sudo umount /mnt/usb

# Option 2: Transfert vers Mac
scp backup_ssd_*.tar.gz ilcamerlingo@IP_DU_MAC:/chemin/backup/

# Vérifier que le backup est bien sur support externe AVANT de continuer
```

### 1.2 Sauvegarde Meshtastic (si applicable)

```bash
# Si tu as des configs Meshtastic
sudo cp -r /var/lib/meshtastic ~/backup_ssd_$(date +%Y%m%d)/ 2>/dev/null || echo "Pas de config Meshtastic"
```

### 1.3 Note des paramètres importants

```bash
# IP actuelle
ip addr show

# Services actifs
systemctl list-units --type=service --state=running > ~/backup_ssd_$(date +%Y%m%d)/services_actifs.txt

# Config réseau
cat /etc/dhcpcd.conf > ~/backup_ssd_$(date +%Y%m%d)/dhcpcd.conf
```

---

## ÉTAPE 2 : Arrêt Propre du Pi

```bash
# Arrêt propre
sudo shutdown -h now

# OU
sudo systemctl poweroff
```

**Attendre que les LEDs s'éteignent complètement avant de débrancher.**

---

## ÉTAPE 3 : Installation Matérielle du SSD

### 3.1 Préparation

1. **Débrancher l'alimentation** du Pi5
2. **Laisser refroidir** 2-3 minutes
3. **Toucher une surface métallique** pour décharger l'électricité statique

### 3.2 Installation du HAT NVMe

| Étape | Action |
|-------|--------|
| 1 | Retirer la vis du connecteur PCIe du Pi5 (si présente) |
| 2 | Aligner le HAT NVMe sur le connecteur PCIe |
| 3 | Enfoncer délicatement jusqu'au clic |
| 4 | Visser le HAT avec les entretoises fournies |
| 5 | Insérer le SSD M.2 dans le slot du HAT |
| 6 | Fixer le SSD avec la vis fournie |

### 3.3 Schéma connexion

```
┌─────────────────┐
│   RASPBERRY     │
│     PI 5        │
│                 │
│  [PCIe]←────────┼─── HAT NVMe
│                 │      │
│                 │   [SSD M.2]
└─────────────────┘
```

---

## ÉTAPE 4 : Installation Système sur SSD

### 4.1 Premier démarrage

1. **Brancher clavier, souris, écran**
2. **Insérer la SD card actuelle** (avec OpenClaw)
3. **Brancher l'alimentation**
4. **Démarrer le Pi**

### 4.2 Vérification du SSD détecté

```bash
# Ouvrir terminal
lsblk

# Tu dois voir quelque chose comme:
# NAME        MAJ:MIN RM   SIZE RO TYPE MOUNTPOINT
# mmcblk0     179:0    0  29.7G  0 disk 
# ├─mmcblk0p1 179:1    0   512M  0 part /boot/firmware
# └─mmcblk0p2 179:2    0  29.2G  0 part /
# nvme0n1     259:0    0 476.9G  0 disk    ← SSD détecté !
```

### 4.3 Copie SD vers SSD (méthode simple)

```bash
# Installer rpi-clone
sudo apt update
sudo apt install -y git

git clone https://github.com/billw2/rpi-clone.git
cd rpi-clone
sudo cp rpi-clone /usr/local/bin/

# Cloner SD vers SSD
sudo rpi-clone nvme0n1

# Suivre les instructions:
# - Confirmer la destination (nvme0n1)
# - Attendre la copie (10-30 min selon taille)

# IMPORTANT: Vérifier les UUID après clonage
# Le clonage change les UUID des partitions
sudo blkid

# Vérifier que /boot/firmware/cmdline.txt pointe vers le bon UUID
sudo cat /boot/firmware/cmdline.txt | grep root=

# Vérifier que /etc/fstab est correct
sudo cat /etc/fstab

# Si nécessaire, corriger avec les nouveaux UUID
sudo nano /boot/firmware/cmdline.txt
sudo nano /etc/fstab
```

### 4.4 Alternative : Installation fraîche

Si tu veux une installation propre:

```bash
# Télécharger Raspberry Pi OS
# https://www.raspberrypi.com/software/

# Utiliser Raspberry Pi Imager sur un autre PC
# Choisir: Raspberry Pi OS 64-bit
# Choisir: SSD NVMe comme destination
# Flasher

# Puis revenir à ce tutoriel pour reconfigurer OpenClaw
```

---

## ÉTAPE 5 : Configuration Boot SSD

### 5.1 Configurer l'ordre de boot (méthode recommandée)

```bash
# Utiliser raspi-config pour définir l'ordre de boot
sudo raspi-config

# Aller dans: Advanced Options → Boot Order → NVMe Boot First
# Valider et redémarrer

# Alternative: Éditer directement l'EEPROM
sudo rpi-eeprom-config --edit

# Ajouter/modifier:
BOOT_ORDER=0xf416  # NVMe first, puis SD, puis USB

# Sauvegarder et redémarrer
sudo reboot
```

### 5.2 Ancienne méthode config.txt (optionnel)

```bash
# Sur Pi5 avec HAT NVMe officiel, dtparam=nvme n'est généralement PAS nécessaire
# Le HAT est reconnu automatiquement

# Si tu utilises un HAT non-officiel ou en cas de problème:
sudo nano /boot/firmware/config.txt

# Décommenter ou ajouter si besoin:
# dtparam=nvme
```

### 5.3 Mettre à jour le firmware (optionnel mais recommandé)

```bash
# Vérifier version actuelle
sudo rpi-eeprom-update

# Mettre à jour si nécessaire
sudo rpi-eeprom-update -a
sudo reboot
```

### 5.4 Tester le boot SSD (méthode sécurisée)

```bash
# IMPORTANT: Garder la SD card en place pour le premier test
# Le Pi bootera sur SSD si configuré correctement, sinon sur SD

# Vérifier le boot actuel
lsblk

# Si nvme0n1p2 est monté sur / → Boot SSD réussi
# Si mmcblk0p2 est monté sur / → Boot encore sur SD

# Une fois le boot SSD validé, tester sans SD:
sudo shutdown -h now
# Retirer la SD card
# Allumer le Pi

# Vérifier:
lsblk
# nvme0n1 doit avoir les partitions montées sur /
```

---

## ÉTAPE 6 : Reconfiguration OpenClaw

### 6.1 Restauration des données

```bash
# Si tu as copié la SD (méthode rpi-clone)
# Tout est déjà là ! Vérifier:
ls -la ~/.openclaw/

# Si installation fraîche, restaurer backup:
cd ~
# Copier backup depuis clé USB ou autre source
tar -xzf backup_ssd_YYYYMMDD.tar.gz
cp -r backup_ssd_YYYYMMDD/.openclaw ~/
```

### 6.2 Vérification services

```bash
# Vérifier OpenClaw
openclaw status

# Si erreurs, vérifier les chemins:
which openclaw
ls -la /usr/local/bin/openclaw*

# Vérifier Node.js
node -v
npm -v

# Vérifier Python
python3 --version
pip3 --version
```

### 6.3 Réinstallation si nécessaire

```bash
# Si OpenClaw manquant
# Restaurer depuis backup complet ou suivre la procédure d'installation
# spécifique à ton environnement (documentation interne)

# NOTE: OpenClaw est un système personnalisé, pas de script public
# Utiliser: tar -xzf backup_openclaw_DATE.tar.gz
# Puis restaurer les configs et services manuellement
```

---

## ÉTAPE 7 : Optimisations SSD

### 7.1 Activer TRIM

```bash
# Vérifier si TRIM est supporté
sudo apt install -y nvme-cli
sudo nvme id-ctrl /dev/nvme0 | grep "Optional Admin Commands"
# Doit contenir "Format"

# Activer TRIM automatique
sudo systemctl enable fstrim.timer
sudo systemctl start fstrim.timer
```

### 7.2 Optimiser fstab

```bash
# Éditer fstab
sudo nano /etc/fstab

# Ajouter noatime aux partitions SSD pour réduire l'usure
# Exemple:
# /dev/nvme0n1p2  /  ext4  defaults,noatime  0  1
```

### 7.3 Désactiver swap (optionnel)

```bash
# Le Pi5 a 16GB RAM, swap peu utile sur SSD
sudo dphys-swapfile swapoff
sudo dphys-swapfile uninstall
sudo systemctl disable dphys-swapfile
```

---

## ÉTAPE 8 : Tests et Validation

### 8.1 Tests de performance

```bash
# Test vitesse SSD
sudo apt install -y hdparm
sudo hdparm -t --direct /dev/nvme0n1

# Résultat attendu: > 300 MB/s (dépend du SSD)

# Test écriture
dd if=/dev/zero of=~/test_speed bs=1M count=1024 conv=fdatasync
rm ~/test_speed
```

### 8.2 Tests OpenClaw

```bash
# Vérifier tous les services
openclaw status

# Tester Telegram
# Envoyer un message de test

# Tester Gateway
curl http://127.0.0.1:18789/health

# Tester agents
openclaw agent list
```

### 8.3 Test de redémarrage

```bash
# Redémarrer et vérifier tout fonctionne
sudo reboot

# Après redémarrage:
openclaw status
lsblk  # Vérifier nvme0n1 bien monté
```

---

## ÉTAPE 9 : Nettoyage Final

### 9.1 Supprimer backup temporaires

```bash
# Nettoyer
rm -rf ~/backup_ssd_*/
rm -f ~/backup_ssd_*.tar.gz

# Conserver uniquement sur support externe
```

### 9.2 Sécuriser la SD card (optionnel)

```bash
# La SD peut servir de rescue
# Ou la formater pour autre usage

# Pour rescue: la garder telle quelle
# Pour réutiliser: formater en FAT32
```

---

## Dépannage

### Problème: SSD non détecté

```bash
# Vérifier connexion physique
# Vérifier dans dmesg:
dmesg | grep -i nvme

# Vérifier alimentation suffisante
# Le HAT NVMe consomme plus de courant
```

### Problème: Boot impossible

```bash
# Remettre la SD card et booter sur SD
# Vérifier l'ordre de boot EEPROM
sudo raspi-config
# Advanced → Boot Order → NVMe Boot First

# Vérifier config.txt (si dtparam=nvme ajouté)
cat /boot/firmware/config.txt | grep nvme

# Vérifier EEPROM
sudo rpi-eeprom-update

# Vérifier les UUID
sudo blkid
sudo cat /boot/firmware/cmdline.txt | grep root=
sudo cat /etc/fstab

# Corriger si nécessaire
sudo nano /boot/firmware/cmdline.txt
sudo nano /etc/fstab
```

### Problème: OpenClaw ne démarre pas

```bash
# Vérifier logs
openclaw logs --follow

# Vérifier permissions
ls -la ~/.openclaw/

# Réinstaller si nécessaire
# (voir backup)
```

---

## Checklist Finale

| Vérification | Statut |
|--------------|--------|
| SSD détecté (`lsblk`) | [ ] |
| Boot sur SSD (pas SD) | [ ] |
| UUID correctement mis à jour | [ ] |
| OpenClaw démarre | [ ] |
| Telegram fonctionne | [ ] |
| Gateway accessible | [ ] |
| Agents disponibles | [ ] |
| TRIM activé | [ ] |
| Backup sécurisé sur support externe | [ ] |
| SD card conservée comme rescue | [ ] |

---

## Ressources

- **Pi5 NVMe HAT**: https://www.raspberrypi.com/products/m2-hat-plus/
- **Raspberry Pi OS**: https://www.raspberrypi.com/software/
- **rpi-clone**: https://github.com/billw2/rpi-clone

---

## Plan d'Action Résumé (par Sonnet)

### Avant de commencer
- [ ] Valider HAT NVMe compatible (M.2 HAT+ officiel recommandé)
- [ ] Préparer destination backup externe (clé USB ou Mac)
- [ ] Vérifier alimentation 27W officielle Pi5

### Pendant l'installation
- [ ] Privilégier rpi-clone avec vérification UUID post-clonage
- [ ] Configurer boot NVMe via raspi-config (pas config.txt)
- [ ] Garder SD card en place pour premier boot test

### Post-installation
- [ ] Valider services OpenClaw un par un
- [ ] Activer TRIM (fstrim.timer) - seule optimisation vraiment utile
- [ ] Conserver SD card comme rescue disk

---

*Document créé le: 2026-03-18*
*Corrections apportées le: 2026-03-18 (relecture Sonnet)*
*Pour: Installation SSD NVMe sur Raspberry Pi 5 avec OpenClaw*
