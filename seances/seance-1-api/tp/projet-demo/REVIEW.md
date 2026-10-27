# Review de la ressource reservations

| Point de contrôle | OK / KO | Ce que j'ai corrigé |
|---|---|---|
| Les codes de statut correspondent à la spec (201, 404, 409) | OK | Création configurée en 201, ressource absente interceptée en 404 et double annulation renvoyant une 409. |
| `response_model` présent sur les 4 routes | OK | `ReservationRead` est bien renseigné sur l'ensemble des quatre routes. |
| La validation `date_fin > date_debut` est bien dans le schéma Pydantic | OK | Copilot avait écrit un `if` avec une `HTTPException(400)` directement dans la route. J'ai supprimé ce code du router et ajouté un `@model_validator(mode="after")` dans `ReservationCreate` pour renvoyer une réponse 422 propre. |
| Le router n'accède pas au stockage de `items` | OK | Copilot a bien créé un dictionnaire `FAKE_DB` local et isolé, sans importer ni modifier celui de `items.py`. |
| Pas d'`async def` sans `await` | OK | Les fonctions sont définies avec de simples `def` synchrones. |
| Aucune dépendance ajoutée dans `requirements.txt` (ou justifiée) | OK | Pas d'autres dépendances ajoutées ; FastAPI et Pydantic suffisent. |
| Les routes littérales sont déclarées avant les routes paramétrées | OK | Les routes de base (`""`) sont bien déclarées au début du fichier avant les routes paramétrées avec `{reservation_id}`, évitant ainsi les conflits de routage. |
| Le code renvoie une réponse cohérente pour `POST /reservations/999/annuler` | OK | La route renvoie correctement une 404 avec un message `detail` explicite. |