// Airbyte Terraform provider documentation: https://registry.terraform.io/providers/airbytehq/airbyte/latest/docs

// Sources
resource "airbyte_source_rss" "source_google_news" {
  configuration = {
    url           = "https://news.google.com/rss/search?q=Gran+Hermano&hl=es-419&gl=AR&ceid=AR:es-419"
    source_type   = "rss"
  }
  name          = "[TF] Google News"
  workspace_id  = var.workspace_id
}
resource "airbyte_source_rss" "source_caras" {
  configuration = {
    url           = "https://caras.perfil.com/feed"
    source_type   = "rss"
  }
  name          = "[TF] Caras"
  workspace_id  = var.workspace_id
}
resource "airbyte_source_rss" "source_exitoina" {
  configuration = {
    url           = "https://exitoina.perfil.com/feed"
    source_type   = "rss"
  }
  name          = "[TF] Exitoina"
  workspace_id  = var.workspace_id
}
resource "airbyte_source_rss" "source_clarin" {
  configuration = {
    url           = "https://www.clarin.com/rss/espectaculos/"
    source_type   = "rss"
  }
  name          = "[TF] Clarin"
  workspace_id  = var.workspace_id
}
resource "airbyte_source_rss" "source_a24" {
  configuration = {
    url           = "https://www.a24.com/rss/pages/trends.xml"
    source_type   = "rss"
  }
  name          = "[TF] A24"
  workspace_id  = var.workspace_id
}
resource "airbyte_source_rss" "source_minuto_uno" {
  configuration = {
    url           = "https://www.minutouno.com/rss/pages/espectaculos.xml"
    source_type   = "rss"
  }
  name          = "[TF] MinutoUno"
  workspace_id  = var.workspace_id
}
resource "airbyte_source_rss" "source_primicias_ya" {
  configuration = {
    url           = "https://www.a24.com/rss/pages/primiciasya.xml"
    source_type   = "rss"
  }
  name          = "[TF] PrimiciasYa"
  workspace_id  = var.workspace_id
}

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
    tunnel_method = {
      destination_postgres_ssh_tunnel_method_no_tunnel = {
        tunnel_method = "NO_TUNNEL"
      }
    }
  }
  name          = "[TF] DB"
  workspace_id  = var.workspace_id
}

// Connections
resource "airbyte_connection" "connection_google_news_db" {
  name                                 = "[TF] Google News -> DB"
  source_id                            = airbyte_source_rss.source_google_news.source_id
  destination_id                       = airbyte_destination_postgres.destination_postgres.destination_id
  non_breaking_schema_updates_behavior = "propagate_columns"
  prefix                               = "tf_google_news_"
  schedule = {
    schedule_type = "cron"
    cron_expression = "0 0 */6 * * ? UTC"
  }
  configurations = {
    streams = [
      {
        name = "items"
        primary_key = [
          [
            "title"
          ]
        ]
        cursor_field = [
          "published"
        ]
        sync_mode = "incremental_deduped_history"
      }
    ]
  }
}
resource "airbyte_connection" "connection_caras_db" {
  name                                 = "[TF] Caras -> DB"
  source_id                            = airbyte_source_rss.source_caras.source_id
  destination_id                       = airbyte_destination_postgres.destination_postgres.destination_id
  non_breaking_schema_updates_behavior = "propagate_columns"
  prefix                               = "tf_caras_"
  schedule = {
    schedule_type = "cron"
    cron_expression = "0 0 */6 * * ? UTC"
  }
  configurations = {
    streams = [
      {
        name = "items"
        primary_key = [
          [
            "title"
          ]
        ]
        cursor_field = [
          "published"
        ]
        sync_mode = "incremental_deduped_history"
      }
    ]
  }
}
resource "airbyte_connection" "connection_exitoina_db" {
  name                                 = "[TF] Exitoina -> DB"
  source_id                            = airbyte_source_rss.source_exitoina.source_id
  destination_id                       = airbyte_destination_postgres.destination_postgres.destination_id
  non_breaking_schema_updates_behavior = "propagate_columns"
  prefix                               = "tf_exitoina_"
  schedule = {
    schedule_type = "cron"
    cron_expression = "0 0 */6 * * ? UTC"
  }
  configurations = {
    streams = [
      {
        name = "items"
        primary_key = [
          [
            "title"
          ]
        ]
        cursor_field = [
          "published"
        ]
        sync_mode = "incremental_deduped_history"
      }
    ]
  }
}
resource "airbyte_connection" "connection_clarin_db" {
  name                                 = "[TF] Clarin -> DB"
  source_id                            = airbyte_source_rss.source_clarin.source_id
  destination_id                       = airbyte_destination_postgres.destination_postgres.destination_id
  non_breaking_schema_updates_behavior = "propagate_columns"
  prefix                               = "tf_clarin_"
  schedule = {
    schedule_type = "cron"
    cron_expression = "0 0 */6 * * ? UTC"
  }
  configurations = {
    streams = [
      {
        name = "items"
        primary_key = [
          [
            "title"
          ]
        ]
        cursor_field = [
          "published"
        ]
        sync_mode = "incremental_deduped_history"
      }
    ]
  }
}
resource "airbyte_connection" "connection_a24_db" {
  name                                 = "[TF] A24 -> DB"
  source_id                            = airbyte_source_rss.source_a24.source_id
  destination_id                       = airbyte_destination_postgres.destination_postgres.destination_id
  non_breaking_schema_updates_behavior = "propagate_columns"
  prefix                               = "tf_a24_"
  schedule = {
    schedule_type = "cron"
    cron_expression = "0 0 */6 * * ? UTC"
  }
  configurations = {
    streams = [
      {
        name = "items"
        primary_key = [
          [
            "title"
          ]
        ]
        cursor_field = [
          "published"
        ]
        sync_mode = "incremental_deduped_history"
      }
    ]
  }
}
resource "airbyte_connection" "connection_minuto_uno_db" {
  name                                 = "[TF] MinutoUno -> DB"
  source_id                            = airbyte_source_rss.source_minuto_uno.source_id
  destination_id                       = airbyte_destination_postgres.destination_postgres.destination_id
  non_breaking_schema_updates_behavior = "propagate_columns"
  prefix                               = "tf_minuto_uno_"
  schedule = {
    schedule_type = "cron"
    cron_expression = "0 0 */6 * * ? UTC"
  }
  configurations = {
    streams = [
      {
        name = "items"
        primary_key = [
          [
            "title"
          ]
        ]
        cursor_field = [
          "published"
        ]
        sync_mode = "incremental_deduped_history"
      }
    ]
  }
}
resource "airbyte_connection" "connection_primicias_ya_db" {
  name                                 = "[TF] PrimiciasYa -> DB"
  source_id                            = airbyte_source_rss.source_primicias_ya.source_id
  destination_id                       = airbyte_destination_postgres.destination_postgres.destination_id
  non_breaking_schema_updates_behavior = "propagate_columns"
  prefix                               = "tf_primicias_ya_"
  schedule = {
    schedule_type = "cron"
    cron_expression = "0 0 */6 * * ? UTC"
  }
  configurations = {
    streams = [
      {
        name = "items"
        primary_key = [
          [
            "title"
          ]
        ]
        cursor_field = [
          "published"
        ]
        sync_mode = "incremental_deduped_history"
      }
    ]
  }
}
