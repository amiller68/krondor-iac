use serde::{Deserialize, Serialize};
use sqlx::encode::IsNull;
use sqlx::error::BoxDynError;
use sqlx::sqlite::{SqliteArgumentValue, SqliteTypeInfo, SqliteValueRef};
use sqlx::{Decode, Encode, Sqlite, Type};

#[derive(Clone, Debug, Deserialize, Serialize)]
#[serde(transparent)]
pub struct Example(String);

impl Example {
    pub fn as_str(&self) -> &str {
        self.0.as_str()
    }
}

impl From<Example> for String {
    fn from(val: Example) -> Self {
        val.0
    }
}

impl From<String> for Example {
    fn from(val: String) -> Self {
        Self(val)
    }
}

impl Decode<'_, Sqlite> for Example {
    fn decode(value: SqliteValueRef<'_>) -> Result<Self, BoxDynError> {
        let db_val = <String as Decode<Sqlite>>::decode(value)?;

        Ok(Self(db_val))
    }
}

impl Encode<'_, Sqlite> for Example {
     fn encode_by_ref(&self, args: &mut Vec<SqliteArgumentValue<'_>>) -> IsNull {
        args.push(SqliteArgumentValue::Text(
            self.0.clone().into()
        ));
        IsNull::No
    }
}

impl Type<Sqlite> for Example {
    fn compatible(ty: &SqliteTypeInfo) -> bool {
        <String as Type<Sqlite>>::compatible(ty)
    }

    fn type_info() -> SqliteTypeInfo {
        <String as Type<Sqlite>>::type_info()
    }
}

#[derive(Debug, thiserror::Error)]
pub enum ExampleError {
    #[error("invalid example: {0}")]
    InvalidExample(String),
}
