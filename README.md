# CrewAI Agent Mania 🤖

Un système multi-agents intelligent basé sur CrewAI pour l'enrichissement et l'analyse automatisée de CV.

## 🎯 Objectif du Projet

Ce projet utilise une architecture multi-agents pour analyser, enrichir et optimiser des CV de manière automatisée, en utilisant la puissance de CrewAI et des modèles de langage avancés.

## 🚀 Fonctionnalités

- Analyse automatique de CV
- Enrichissement de contenu
- Système multi-agents collaboratif
- Traitement de données structurées et non structurées
- Génération de graphiques d'analyse

## 🛠️ Structure du Projet

```
├── CV/                     # Dossier contenant les CV à analyser
├── cv_enrichment_complete/ # Résultats d'enrichissement
├── db/                     # Base de données
├── tools_llm/             # Outils basés sur les modèles de langage
├── tools_vanilla/         # Outils classiques
├── agents.py              # Définition des agents
├── tasks.py               # Définition des tâches
├── main.py               # Point d'entrée principal
└── multiplecrew.py       # Gestion des équipes d'agents
```

## 📋 Prérequis

- Python 3.8+
- CrewAI
- Autres dépendances listées dans requirements.txt

## 🔧 Installation

1. Clonez le repository :
```bash
git clone https://github.com/Magomin/sma-crewai-agentmania.git
cd sma-crewai-agentmania
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Configurez le fichier config.json avec vos paramètres

## 💻 Utilisation

1. Placez les CV à analyser dans le dossier `CV/`

2. Lancez le script principal :
```bash
python main.py
```

3. Les résultats enrichis seront disponibles dans le dossier `cv_enrichment_complete/`

## 📊 Visualisation

Le projet inclut des capacités de visualisation avec la génération de graphiques d'analyse ((graph)cv_enrichement.png).

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue
- Proposer une pull request
- Suggérer des améliorations

## 📝 License

MIT License

## 📫 Contact

Pour toute question ou suggestion, n'hésitez pas à ouvrir une issue sur le repository.
