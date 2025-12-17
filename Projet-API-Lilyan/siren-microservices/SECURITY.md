# Politique de Sécurité - Siren Microservices

## 🔒 Gestion des Secrets et Credentials

### Principe de base
**JAMAIS de credentials hardcodés dans le code ou les Dockerfiles.**

Toutes les informations sensibles (mots de passe, secrets, clés API) doivent être:
- Stockées dans des variables d'environnement
- Gérées via le fichier `.env` (développement) ou un gestionnaire de secrets (production)
- Exclues du contrôle de version (`.gitignore`)

---

## 📋 Checklist de Sécurité

### Avant de committer
- [ ] Aucun mot de passe dans le code source
- [ ] Aucune clé API hardcodée
- [ ] Le fichier `.env` est dans `.gitignore`
- [ ] Les Dockerfiles n'exposent pas de credentials
- [ ] Les logs ne contiennent pas de mots de passe

### Avant le déploiement en production
- [ ] Tous les mots de passe par défaut ont été changés
- [ ] Les mots de passe sont forts (12+ caractères, mixte)
- [ ] Chaque environnement a des credentials uniques
- [ ] HTTPS est activé sur tous les endpoints
- [ ] Les secrets sont gérés par un gestionnaire dédié (Vault, AWS Secrets Manager, etc.)
- [ ] Rate limiting activé sur les endpoints d'authentification
- [ ] Les logs de production sont nettoyés des informations sensibles

---

## 🔑 Variables d'Environnement Sensibles

### Secrets critiques (à changer OBLIGATOIREMENT en production)

| Variable | Type | Importance | Recommandation |
|----------|------|------------|----------------|
| `MYSQL_ROOT_PASSWORD` | Mot de passe | **CRITIQUE** | 32+ caractères, aléatoire |
| `MYSQL_PASSWORD` | Mot de passe | **CRITIQUE** | 24+ caractères, unique |
| `OAUTH2_CLIENT_SECRET` | Secret | **CRITIQUE** | 32+ caractères, aléatoire |
| `OAUTH2_USER1` | Credentials | **HAUTE** | Mot de passe fort, unique |
| `OAUTH2_USER2` | Credentials | **HAUTE** | Mot de passe fort, unique |

### Génération de mots de passe sécurisés

```bash
# Avec OpenSSL (recommandé)
openssl rand -base64 32

# Avec Python
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Avec Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

---

## 🛡️ Bonnes Pratiques par Environnement

### Développement Local
- ✅ Utiliser le fichier `.env` fourni (valeurs par défaut acceptables)
- ✅ Chaque développeur peut avoir son propre `.env`
- ✅ Ne JAMAIS committer le `.env`
- ✅ Documenter toutes les variables dans `.env.example`

### Staging / Pré-production
- ✅ Credentials différents de la production
- ✅ Rotation des secrets tous les 90 jours
- ✅ Accès limité à l'équipe technique
- ✅ Logs d'audit activés

### Production
- ✅ Utiliser un gestionnaire de secrets (Vault, AWS Secrets Manager, Azure Key Vault)
- ✅ Rotation automatique des secrets (30-90 jours)
- ✅ Authentification multi-facteurs (MFA) pour les accès administrateurs
- ✅ Chiffrement au repos et en transit (TLS 1.3+)
- ✅ Monitoring des accès et alertes sur activités suspectes
- ✅ Principe du moindre privilège (least privilege)

---

## 🚨 Que Faire en Cas de Fuite de Credentials

### Action immédiate (dans l'heure)
1. **Révoquer immédiatement** tous les credentials exposés
2. **Générer de nouveaux** secrets forts
3. **Redéployer** les services avec les nouveaux credentials
4. **Notifier** l'équipe de sécurité

### Investigation (dans les 24h)
5. **Auditer** les logs pour détecter des accès non autorisés
6. **Identifier** la source de la fuite (commit git, logs, etc.)
7. **Nettoyer** l'historique git si nécessaire (`git filter-repo`)
8. **Documenter** l'incident

### Prévention
9. **Réviser** les processus de développement
10. **Former** l'équipe sur les bonnes pratiques
11. **Mettre en place** des pre-commit hooks (détection de secrets)
12. **Scanner** régulièrement le code avec des outils (GitGuardian, TruffleHog)

---

## 🔍 Outils de Détection

### Pre-commit Hooks
```bash
# Installer detect-secrets
pip install detect-secrets

# Scanner le repository
detect-secrets scan > .secrets.baseline

# Auditer les résultats
detect-secrets audit .secrets.baseline
```

### GitGuardian (GitHub/GitLab)
- Surveillance en temps réel des commits
- Alertes automatiques sur fuites de secrets
- Intégration CI/CD

### TruffleHog
```bash
# Scanner l'historique git
trufflehog git file://. --only-verified
```

---

## 📚 Ressources

### Documentation
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [NIST Password Guidelines](https://pages.nist.gov/800-63-3/sp800-63b.html)
- [12 Factor App - Config](https://12factor.net/config)

### Gestionnaires de Secrets Recommandés
- **HashiCorp Vault**: Self-hosted, open-source
- **AWS Secrets Manager**: Cloud AWS
- **Azure Key Vault**: Cloud Azure
- **Google Secret Manager**: Cloud GCP
- **Doppler**: SaaS multi-cloud

---

## 📞 Contact Sécurité

Pour signaler une vulnérabilité de sécurité:
- **Email**: security@example.com
- **PGP Key**: [Fournir la clé publique]
- **Bug Bounty**: [Lien vers le programme si existant]

**Merci de nous signaler les vulnérabilités de manière responsable.**

---

## 📝 Changelog Sécurité

### 2024-12-17
- ✅ Migration des credentials vers variables d'environnement
- ✅ Suppression de tous les mots de passe hardcodés
- ✅ Ajout du fichier `.env.example`
- ✅ Documentation de la gestion des secrets
- ✅ Mise à jour des Dockerfiles (suppression credentials)

### Prochaines Améliorations
- [ ] Intégration avec HashiCorp Vault
- [ ] Rotation automatique des secrets
- [ ] Authentification multi-facteurs (MFA)
- [ ] Chiffrement de la base de données au repos
- [ ] Implémentation de rate limiting
- [ ] Audit logging complet
