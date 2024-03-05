// Airbyte Terraform provider documentation: https://registry.terraform.io/providers/airbytehq/airbyte/latest/docs

// Sources

// Destinations
resource "airbyte_destination_postgres" "destination_postgres" {
  configuration = {
    database            = "news"
    username            = "news"
    password            = "news"
    schema              = "public"
    destination_type    = "postgres"
    host                = "localhost"
    port                = 5432
    ssl_mode = {
      destination_postgres_ssl_modes_disable = {
        mode = "disable"
      }
    }
  }
  name          = "DB"
  workspace_id  = var.workspace_id
}

// Connections
