from pymongo import MongoClient
from datetime import datetime
from mongoengine import *

# Configurer la connexion à MongoDB avec mongoengine
connect('database_intervention', host='localhost', port=27017)

class Intervenant(Document):
    prenom = StringField(required=True)
    nom = StringField(required=True)
    departement_service = StringField(required=True)

class DemandeIntervention(Document):

    date_emission = DateTimeField(default=datetime.utcnow)
    intervenant = ReferenceField(Intervenant, required=True)
    nom = StringField(required=True)
    prenom = StringField(required=True)
    departement_service = StringField(required=True)
    nature = StringField(required=True)
    anomalie_detectee = StringField(required=True)
    recommandation = StringField()
    date_intervention = DateTimeField()
    type_prestation = StringField()
    observations = StringField()
    resultat = StringField()
    affiche_path = StringField(required=True)  

exemples_intervenants = [
    {'prenom': 'Ahmed', 'nom': 'Benjelloun', 'departement_service': 'Département IT'},
    {'prenom': 'Fatima', 'nom': 'Zahraoui', 'departement_service': 'Département Maintenance'},
    {'prenom': 'Mohammed', 'nom': 'El Fassi', 'departement_service': 'Département Logistique'},
    {'prenom': 'Nadia', 'nom': 'Berrada', 'departement_service': 'Département RH'},
    {'prenom': 'Omar', 'nom': 'Chakir', 'departement_service': 'Département Communication'},
    {'prenom': 'Sanaa', 'nom': 'Abdi', 'departement_service': 'Département Finances'},
    {'prenom': 'Youssef', 'nom': 'El Mekki', 'departement_service': 'Département Sécurité'},
    {'prenom': 'Amina', 'nom': 'Bouhaddou', 'departement_service': 'Département Juridique'},
    {'prenom': 'Hicham', 'nom': 'Ouazzani', 'departement_service': 'Département Infrastructures'},
    {'prenom': 'Loubna', 'nom': 'Hamdi', 'departement_service': 'Département Formation'}
]

# Insérer les intervenants dans la base de données
intervenants_docs = []
for intervenant in exemples_intervenants:
    intervenant_doc = Intervenant(**intervenant).save()
    intervenants_docs.append(intervenant_doc)

# Exemple de correspondance entre les noms et les objets Intervenant
nom_to_intervenant = {f"{intervenant.prenom} {intervenant.nom}": intervenant for intervenant in intervenants_docs}

# Exemples de demandes d'intervention pour chaque intervenant
exemples_demandes = [
    {
        'date_emission': datetime(2024, 7, 1),
        'intervenant': nom_to_intervenant['Ahmed Benjelloun'],
        'prenom': 'Ahmed',
        'nom': 'Benjelloun',
        'departement_service': 'Département IT',
        'nature': 'Maintenance corrective',
        'anomalie_detectee': 'Panne de serveur',
        'recommandation': 'Remplacer le disque dur défectueux',
        'date_intervention': datetime(2024, 7, 2),
        'type_prestation': 'Réparation',
        'observations': 'Aucune observation',
        'resultat': 'Réussite',
        'affiche_path': 'C:\\Users\\Downloads\\Desktop'
        
    },
    {
        'date_emission': datetime(2024, 7, 5),
        'intervenant': nom_to_intervenant['Fatima Zahraoui'],
        'prenom': 'Fatima',
        'nom': 'Zahraoui',
        'departement_service': 'Département Maintenance',
        'nature': 'Maintenance préventive',
        'anomalie_detectee': 'Aucune anomalie détectée',
        'recommandation': 'Effectuer une vérification régulière',
        'date_intervention': datetime(2024, 7, 7),
        'type_prestation': 'Maintenance',
        'observations': 'Aucune observation',
        'resultat': 'Réussite',
        'affiche_path': 'C:\\Users\\Downloads\\Desktop'
    },
    {
        'date_emission': datetime(2024, 7, 10),
        'intervenant': nom_to_intervenant['Mohammed El Fassi'],
        'prenom': 'Mohammed',
        'nom': 'El Fassi',
        'departement_service': 'Département Logistique',
        'nature': 'Support utilisateur',
        'anomalie_detectee': 'Problème d\'accès au réseau',
        'recommandation': 'Configurer correctement les paramètres réseau',
        'date_intervention': datetime(2024, 7, 12),
        'type_prestation': 'Assistance',
        'observations': 'Besoin de formation supplémentaire',
        'resultat': 'Échec',
        'affiche_path': 'C:\\Users\\Downloads\\Desktop'
    },
    {
        'date_emission': datetime(2024, 7, 15),
        'intervenant': nom_to_intervenant['Nadia Berrada'],
        'prenom': 'Nadia',
        'nom': 'Berrada',
        'departement_service': 'Département RH',
        'nature': 'Maintenance corrective',
        'anomalie_detectee': 'Problème d\'impression',
        'recommandation': 'Remplacer le tambour d\'impression',
        'date_intervention': datetime(2024, 7, 17),
        'type_prestation': 'Réparation',
        'observations': 'Pièce de rechange commandée',
        'resultat': 'Réussite',
        'affiche_path':'C:\\Users\\Downloads\\Desktop'
    },
    {
        'date_emission': datetime(2024, 7, 20),
        'intervenant': nom_to_intervenant['Omar Chakir'],
        'prenom': 'Omar',
        'nom': 'Chakir',
        'departement_service': 'Département Communication',
        'nature': 'Audit de sécurité',
        'anomalie_detectee': 'Faille de sécurité détectée',
        'recommandation': 'Mise à jour des pare-feu et antivirus',
        'date_intervention': datetime(2024, 7, 22),
        'type_prestation': 'Audit',
        'observations': 'Rapport d\'audit soumis à la direction',
        'resultat': 'Réussite',
        'affiche_path':'C:\\Users\\Downloads\\Desktop'
    },
    {
        'date_emission': datetime(2024, 7, 25),
        'intervenant': nom_to_intervenant['Sanaa Abdi'],
        'prenom': 'Sanaa',
        'nom': 'Abdi',
        'departement_service': 'Département Finances',
        'nature': 'Installation de matériel',
        'anomalie_detectee': 'Nouvelle machine à installer',
        'recommandation': 'Configurer selon les spécifications du client',
        'date_intervention': datetime(2024, 7, 27),
        'type_prestation': 'Installation',
        'observations': 'Formation des utilisateurs effectuée',
        'resultat': 'Réussite',
        'affiche_path': 'C:\\Users\\Downloads\\Desktop'
    },
    {
        'date_emission': datetime(2024, 7, 30),
        'intervenant': nom_to_intervenant['Youssef El Mekki'],
        'prenom': 'Youssef',
        'nom': 'El Mekki',
        'departement_service': 'Département Sécurité',
        'nature': 'Maintenance préventive',
        'anomalie_detectee': 'Aucune anomalie détectée',
        'recommandation': 'Vérification des sauvegardes',
        'date_intervention': datetime(2024, 8, 1),
        'type_prestation': 'Maintenance',
        'observations': 'Aucune observation',
        'resultat': 'Réussite',
        'affiche_path': 'C:\\Users\\Downloads\\Desktop'
    },
    {
        'date_emission': datetime(2024, 8, 5),
        'intervenant': nom_to_intervenant['Amina Bouhaddou'],
        'prenom': 'Amina',
        'nom': 'Bouhaddou',
        'departement_service': 'Département Juridique',
        'nature': 'Support utilisateur',
        'anomalie_detectee': 'Problème de logiciel',
        'recommandation': 'Réinstaller le logiciel',
        'date_intervention': datetime(2024, 8, 7),
        'type_prestation': 'Assistance',
        'observations': 'Client satisfait du service',
        'resultat': 'Réussite',
        'affiche_path': 'C:\\Users\\Downloads\\Desktop'
    },
    {
        'date_emission': datetime(2024, 8, 10),
        'intervenant': nom_to_intervenant['Hicham Ouazzani'],
        'prenom': 'Hicham',
        'nom': 'Ouazzani',
        'departement_service': 'Département Infrastructures',
        'nature': 'Maintenance corrective',
        'anomalie_detectee': 'Panne d\'électricité',
        'recommandation': 'Vérifier le tableau électrique',
        'date_intervention': datetime(2024, 8, 12),
        'type_prestation': 'Réparation',
        'observations': 'Besoin de matériel de remplacement',
        'resultat': 'Réussite',
        'affiche_path': 'C:\\Users\\Downloads\\Desktop'
    },
    {
        'date_emission': datetime(2024, 8, 15),
        'intervenant': nom_to_intervenant['Loubna Hamdi'],
        'prenom': 'Loubna',
        'nom': 'Hamdi',
        'departement_service': 'Département Formation',
        'nature': 'Audit de performance',
        'anomalie_detectee': 'Baisse de performance du serveur',
        'recommandation': 'Optimiser les configurations du serveur',
        'date_intervention': datetime(2024, 8, 17),
        'type_prestation': 'Audit',
        'observations': 'Analyse des performances effectuée',
        'resultat': 'Réussite',
        'affiche_path': 'C:\\Users\\Downloads\\Desktop'
    }
]

# Insérer des exemples de demandes d'intervention avec les informations d'intervenant
for exemple_demande in exemples_demandes:
    demande_intervention = DemandeIntervention(
        date_emission=exemple_demande['date_emission'],
        intervenant=exemple_demande['intervenant'],
        prenom=exemple_demande['prenom'],
        nom=exemple_demande['nom'],
        departement_service=exemple_demande['departement_service'],
        nature=exemple_demande['nature'],
        anomalie_detectee=exemple_demande['anomalie_detectee'],
        recommandation=exemple_demande['recommandation'],
        date_intervention=exemple_demande['date_intervention'],
        type_prestation=exemple_demande['type_prestation'],
        observations=exemple_demande['observations'],
        resultat=exemple_demande['resultat'],
        affiche_path=exemple_demande['affiche_path']  # Assurez-vous que ce champ est bien spécifié
    )
    demande_intervention.save()


print("Exemples de demandes d'intervention insérés avec succès.")
