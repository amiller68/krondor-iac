use axum::extract::FromRef;

use super::config::Config;

use crate::database::Database;

#[derive(Clone)]
pub struct AppState {
    sqlite_database: Database,
}

impl AppState {
    pub async fn from_config(config: &Config) -> Result<Self, AppStateSetupError> {
        let sqlite_database = Database::connect(&config.sqlite_database_url()).await?;

        Ok(Self { sqlite_database })
    }

    pub fn sqlite_database(&self) -> Database {
        self.sqlite_database.clone()
    }
}

impl FromRef<AppState> for Database {
    fn from_ref(state: &AppState) -> Self {
        state.sqlite_database()
    }
}

#[derive(Debug, thiserror::Error)]
pub enum AppStateSetupError {
    #[error("error occurred while attempting to setup the database: {0}")]
    DatabaseSetupError(#[from] crate::database::DatabaseSetupError),
    // TODO: register state setup errors here
}
