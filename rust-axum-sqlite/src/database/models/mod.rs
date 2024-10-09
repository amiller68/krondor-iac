use sqlx::FromRow;

use crate::database::types::ExampleType;
use crate::database::DatabaseConnection;

/*
CREATE TABLE examples (
    id SERIAL PRIMARY KEY,
    example TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE UNIQUE INDEX unique_examples ON examples (example);
*/

#[derive(FromRow, Debug)]
pub struct ExampleModel {
    example: ExampleType,
}

impl ExampleModel {
    pub async fn create(
        example: String,
        conn: &mut DatabaseConnection,
    ) -> Result<ExampleModel, ExampleModelError> { 
        // Read the current root cid
        let example_type: ExampleType = example.into();
        let example_model = sqlx::query_as!(
            ExampleModel,
            r#"
            INSERT INTO examples (
                example
            )
            VALUES (
                $1
            )
            RETURNING example as "example: ExampleType"
            "#,
            example_type
        )
        .fetch_one(conn)
        .await
        .map_err(|e| match e {
            sqlx::Error::Database(ref db_error) => {
                if db_error.constraint().unwrap_or("") == "unique_examples" {
                    ExampleModelError::Conflict(example_type.as_str().to_string())
                } else {
                    e.into()
                }
            }
            _ => e.into(),
        })?;
        Ok(example_model)
    }

    pub fn example(&self) -> &str {
        self.example.as_str()
    }
}

#[derive(Debug, thiserror::Error)]
pub enum ExampleModelError {
    #[error("sqlx: {0}")]
    Sqlx(#[from] sqlx::Error),
    #[error("conflict: {0}")]
    Conflict(String),
}
