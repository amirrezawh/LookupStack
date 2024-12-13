locals {
  chosen_image = try(
    [for image in data.arvan_images.terraform_image.distributions : image
    if image.distro_name == var.distro_name && image.name == var.distro_version],
    []
  )

  selected_plan = [for plan in data.arvan_plans.plan_list.plans : plan if plan.id == var.plan_id][0]

  network_list = tolist(data.arvan_networks.terraform_network.networks)

  chosen_network = try(
    [for network in local.network_list : network if network.name == var.network_name],
    []
  )
}