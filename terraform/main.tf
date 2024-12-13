terraform {
  required_providers {
    arvan = {
      source = "terraform.arvancloud.ir/arvancloud/iaas"
    }
  }
}

provider "arvan" {
  api_key = "apikey"
}

resource "arvan_security_group" "terraform_security_group" {
  region      = var.region
  description = "Terraform-created security group"
  name        = "tf_security_group"
  rules = [
    {
      direction = "ingress"
      protocol  = "icmp"
    },
    {
      direction = "ingress"
      protocol  = "udp"
    },
    {
      direction = "ingress"
      protocol  = "tcp"
    },
    {
      direction = "egress"
      protocol  = ""
    }
  ]
}

resource "arvan_abrak" "built_by_terraform" {
  depends_on = [arvan_security_group.terraform_security_group]

  timeouts {
    create = "1h30m"
    update = "2h"
    delete = "20m"
    read   = "10m"
  }

  region    = var.region
  name      = "node-${count.index + 1}"
  count     = 3
  image_id  = local.chosen_image[0].id
  flavor_id = local.selected_plan.id
  disk_size = 25

  networks = [
    {
      network_id = local.chosen_network[0].network_id
    }
  ]

  security_groups = [arvan_security_group.terraform_security_group.id]
}



