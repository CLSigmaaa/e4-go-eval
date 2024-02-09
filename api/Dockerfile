# Utilisation de l'image officielle de Go 1.16.6 comme image de base
FROM golang:1.21.6

# Définir le répertoire de travail à l'intérieur du conteneur
WORKDIR /app

# Copier le contenu de votre application Go dans le conteneur
COPY . .

# Compiler l'application
RUN go build -o main .

# Exposer le port sur lequel votre application écoute
EXPOSE 3000

# Commande à exécuter lors du démarrage du conteneur
CMD ["./main"]