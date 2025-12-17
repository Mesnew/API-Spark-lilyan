/**
 * In-Memory Model pour OAuth2
 * ATTENTION: À utiliser uniquement pour le développement/test, PAS EN PRODUCTION
 */

function InMemoryModel() {
  // Clients OAuth2 (applications autorisées)
  const clientId = process.env.OAUTH2_CLIENT_ID || 'client-app';
  const clientSecret = process.env.OAUTH2_CLIENT_SECRET || 'default_secret_change_me';

  this.clients = [
    {
      clientId: clientId,
      clientSecret: clientSecret,
      redirectUris: ['http://localhost:3000/callback'],
      grants: ['password', 'refresh_token', 'client_credentials']
    }
  ];

  // Tokens générés
  this.tokens = [];

  // Utilisateurs de l'application (chargés depuis variables d'environnement)
  this.users = [];

  // Parser OAUTH2_USER1 (format: "username:password")
  if (process.env.OAUTH2_USER1) {
    const [username, password] = process.env.OAUTH2_USER1.split(':');
    if (username && password) {
      this.users.push({ id: '1', username, password });
    }
  } else {
    // Valeur par défaut (DEV uniquement)
    this.users.push({ id: '1', username: 'user1', password: 'default_pass_1' });
  }

  // Parser OAUTH2_USER2 (format: "username:password")
  if (process.env.OAUTH2_USER2) {
    const [username, password] = process.env.OAUTH2_USER2.split(':');
    if (username && password) {
      this.users.push({ id: '2', username, password });
    }
  } else {
    // Valeur par défaut (DEV uniquement)
    this.users.push({ id: '2', username: 'user2', password: 'default_pass_2' });
  }

  console.log('OAuth2 Model initialized with:');
  console.log(`- Client ID: ${clientId}`);
  console.log(`- Users: ${this.users.map(u => u.username).join(', ')}`);
}

/**
 * Dump du cache pour debug
 */
InMemoryModel.prototype.dump = function() {
  console.log('=== OAuth2 Memory Store ===');
  console.log('Clients:', this.clients);
  console.log('Tokens:', this.tokens);
  console.log('Users:', this.users.map(u => ({ id: u.id, username: u.username })));
  console.log('===========================');
};

/**
 * Récupérer un access token
 */
InMemoryModel.prototype.getAccessToken = function(accessToken) {
  const tokens = this.tokens.filter(token => token.accessToken === accessToken);

  if (!tokens.length) {
    return false;
  }

  const token = tokens[0];
  return {
    accessToken: token.accessToken,
    accessTokenExpiresAt: token.accessTokenExpiresAt,
    client: { id: token.clientId },
    user: { id: token.userId }
  };
};

/**
 * Récupérer un refresh token
 */
InMemoryModel.prototype.getRefreshToken = function(refreshToken) {
  const tokens = this.tokens.filter(token => token.refreshToken === refreshToken);

  if (!tokens.length) {
    return false;
  }

  const token = tokens[0];
  return {
    refreshToken: token.refreshToken,
    refreshTokenExpiresAt: token.refreshTokenExpiresAt,
    client: { id: token.clientId },
    user: { id: token.userId }
  };
};

/**
 * Récupérer un client
 */
InMemoryModel.prototype.getClient = function(clientId, clientSecret) {
  const clients = this.clients.filter(client => {
    return client.clientId === clientId &&
           (clientSecret ? client.clientSecret === clientSecret : true);
  });

  if (!clients.length) {
    return false;
  }

  return clients[0];
};

/**
 * Sauvegarder un token
 */
InMemoryModel.prototype.saveToken = function(token, client, user) {
  const savedToken = {
    accessToken: token.accessToken,
    accessTokenExpiresAt: token.accessTokenExpiresAt,
    refreshToken: token.refreshToken,
    refreshTokenExpiresAt: token.refreshTokenExpiresAt,
    clientId: client.clientId,
    userId: user.id
  };

  this.tokens.push(savedToken);

  // Retourner le token avec les références client et user
  return {
    accessToken: savedToken.accessToken,
    accessTokenExpiresAt: savedToken.accessTokenExpiresAt,
    refreshToken: savedToken.refreshToken,
    refreshTokenExpiresAt: savedToken.refreshTokenExpiresAt,
    client: { id: client.clientId },
    user: { id: user.id }
  };
};

/**
 * Récupérer un utilisateur (pour le grant type "password")
 */
InMemoryModel.prototype.getUser = function(username, password) {
  const users = this.users.filter(user => {
    return user.username === username && user.password === password;
  });

  if (!users.length) {
    return false;
  }

  return users[0];
};

/**
 * Révoquer un refresh token
 */
InMemoryModel.prototype.revokeToken = function(token) {
  const index = this.tokens.findIndex(t => t.refreshToken === token.refreshToken);

  if (index !== -1) {
    this.tokens.splice(index, 1);
    return true;
  }

  return false;
};

/**
 * Récupérer les user credentials (pour le grant type "client_credentials")
 */
InMemoryModel.prototype.getUserFromClient = function(client) {
  // Pour le client credentials grant, on retourne un utilisateur système
  return {
    id: 'system'
  };
};

/**
 * Vérifier le scope (optionnel, simplifié ici)
 */
InMemoryModel.prototype.verifyScope = function(token, scope) {
  // Implémentation simplifiée - accepte tous les scopes
  return true;
};

module.exports = InMemoryModel;
