# Assistant Académique Intelligent — Base de Connaissances

## Component: module_inscription

### Block: bloc_inscription_cours

#### Function: verifier_prerequis
Vérifie si l'étudiant a les prérequis nécessaires avant de s'inscrire à un cours.
Un étudiant doit avoir validé au moins 60% des crédits du semestre précédent.

#### Function: inscrire_etudiant
Permet d'inscrire un étudiant à un cours disponible.
L'inscription est possible uniquement pendant la période officielle définie par l'administration.

#### Function: annuler_inscription
Permet d'annuler une inscription dans un délai de 7 jours après la date limite d'inscription.

#### Data: liste_cours_disponibles
Contient la liste de tous les cours disponibles par semestre, avec les places restantes.

---

## Component: module_notes

### Block: bloc_consultation_notes

#### Function: consulter_notes
Permet à un étudiant de consulter ses notes par matière et par semestre.
Les notes sont disponibles 48h après la délibération du jury.

#### Function: contester_note
Un étudiant peut contester une note dans un délai de 15 jours après publication.
La contestation doit être motivée et soumise au responsable pédagogique.

#### Data: historique_notes
Contient l'historique complet des notes de l'étudiant depuis son entrée dans l'établissement.

---

## Component: module_rh_remboursement

### Block: bloc_remboursement_frais

#### Function: soumettre_demande_remboursement
Permet à un étudiant de soumettre une demande de remboursement pour des frais engagés.
Les justificatifs originaux doivent être fournis dans un délai de 30 jours.

#### Function: suivre_remboursement
Permet de suivre l'état d'avancement d'une demande de remboursement.
Les délais de traitement sont de 15 jours ouvrables après réception du dossier complet.

#### Function: annuler_remboursement
Permet d'annuler une demande de remboursement non encore traitée.

#### Data: barème_remboursement
Contient les montants maximaux remboursables par catégorie de frais (transport, matériel, etc.).

---

## Component: module_bibliotheque

### Block: bloc_emprunt_livres

#### Function: rechercher_livre
Permet de rechercher un livre dans le catalogue de la bibliothèque par titre, auteur ou ISBN.

#### Function: emprunter_livre
Un étudiant peut emprunter jusqu'à 5 livres simultanément pour une durée de 21 jours.

#### Function: renouveler_emprunt
Permet de renouveler un emprunt une seule fois si le livre n'est pas réservé par un autre étudiant.

#### Data: catalogue_livres
Contient la liste complète des livres disponibles avec leur statut (disponible, emprunté, réservé).

---

## Component: module_connexion

### Block: bloc_authentification

#### Function: connexion_etudiant
Permet à un étudiant de se connecter avec son identifiant et mot de passe.
En cas d'échec après 3 tentatives, le compte est temporairement verrouillé pour 15 minutes.

#### Function: reinitialiser_mot_de_passe
Permet de réinitialiser le mot de passe via l'email institutionnel de l'étudiant.

#### Function: deconnexion
Termine la session de l'étudiant de manière sécurisée.

#### Access: acces_admin
Réservé aux administrateurs et responsables pédagogiques uniquement.