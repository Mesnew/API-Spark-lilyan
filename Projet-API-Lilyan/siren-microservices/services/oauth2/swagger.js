/**
 * Configuration Swagger/OpenAPI pour l'API OAuth2
 */

const swaggerJsdoc = require('swagger-jsdoc');

const options = {
  definition: {
    openapi: '3.0.0',
    info: {
      title: 'OAuth2 Server API',
      version: '1.0.0',
      description: 'API OAuth2 pour l\'authentification et l\'autorisation des services',
      contact: {
        name: 'API Support',
        email: 'support@example.com'
      },
      license: {
        name: 'ISC',
        url: 'https://opensource.org/licenses/ISC'
      }
    },
    servers: [
      {
        url: 'http://localhost:3000',
        description: 'Serveur de développement'
      },
      {
        url: 'http://oauth2:3000',
        description: 'Serveur Docker'
      }
    ],
    components: {
      securitySchemes: {
        bearerAuth: {
          type: 'http',
          scheme: 'bearer',
          bearerFormat: 'OAuth2'
        },
        oauth2Password: {
          type: 'oauth2',
          flows: {
            password: {
              tokenUrl: '/oauth/token',
              scopes: {}
            },
            clientCredentials: {
              tokenUrl: '/oauth/token',
              scopes: {}
            }
          }
        }
      },
      schemas: {
        TokenRequest: {
          type: 'object',
          required: ['grant_type', 'client_id', 'client_secret'],
          properties: {
            grant_type: {
              type: 'string',
              enum: ['password', 'client_credentials', 'refresh_token'],
              description: 'Type de grant OAuth2'
            },
            client_id: {
              type: 'string',
              example: 'client-app',
              description: 'ID du client'
            },
            client_secret: {
              type: 'string',
              example: 'secret123',
              description: 'Secret du client'
            },
            username: {
              type: 'string',
              example: 'user1',
              description: 'Nom d\'utilisateur (requis pour grant_type=password)'
            },
            password: {
              type: 'string',
              example: 'password123',
              description: 'Mot de passe (requis pour grant_type=password)'
            },
            refresh_token: {
              type: 'string',
              description: 'Refresh token (requis pour grant_type=refresh_token)'
            }
          }
        },
        TokenResponse: {
          type: 'object',
          properties: {
            accessToken: {
              type: 'string',
              description: 'Token d\'accès OAuth2'
            },
            accessTokenExpiresAt: {
              type: 'string',
              format: 'date-time',
              description: 'Date d\'expiration du token d\'accès'
            },
            refreshToken: {
              type: 'string',
              description: 'Token de rafraîchissement'
            },
            refreshTokenExpiresAt: {
              type: 'string',
              format: 'date-time',
              description: 'Date d\'expiration du refresh token'
            },
            client: {
              type: 'object',
              properties: {
                id: {
                  type: 'string',
                  description: 'ID du client'
                }
              }
            },
            user: {
              type: 'object',
              properties: {
                id: {
                  type: 'string',
                  description: 'ID de l\'utilisateur'
                }
              }
            }
          }
        },
        User: {
          type: 'object',
          properties: {
            id: {
              type: 'string',
              description: 'ID de l\'utilisateur'
            },
            username: {
              type: 'string',
              description: 'Nom d\'utilisateur'
            }
          }
        },
        UserList: {
          type: 'object',
          properties: {
            users: {
              type: 'array',
              items: {
                $ref: '#/components/schemas/User'
              }
            }
          }
        },
        Error: {
          type: 'object',
          properties: {
            error: {
              type: 'string',
              description: 'Type d\'erreur'
            },
            error_description: {
              type: 'string',
              description: 'Description de l\'erreur'
            }
          }
        },
        Health: {
          type: 'object',
          properties: {
            status: {
              type: 'string',
              example: 'OK'
            },
            message: {
              type: 'string',
              example: 'OAuth2 Server is running'
            },
            timestamp: {
              type: 'string',
              format: 'date-time'
            }
          }
        }
      }
    },
    tags: [
      {
        name: 'OAuth2',
        description: 'Endpoints OAuth2 pour l\'authentification'
      },
      {
        name: 'Users',
        description: 'Gestion des utilisateurs'
      },
      {
        name: 'Health',
        description: 'Santé du serveur'
      },
      {
        name: 'Debug',
        description: 'Endpoints de débogage (développement uniquement)'
      }
    ]
  },
  apis: ['./app.js']
};

const swaggerSpec = swaggerJsdoc(options);

module.exports = swaggerSpec;
