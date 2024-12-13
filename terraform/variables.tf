variable "region" {
  type        = string
  description = "The chosen region for resources"
  default     = "ir-thr-ba1"
}

variable "distro_name" {
  type        = string
  description = "The chosen distro name for the image"
  default     = "ubuntu"
}

variable "distro_version" {
  type        = string
  description = "The chosen release for the image"
  default     = "22.04"
}

variable "network_name" {
  type        = string
  description = "The chosen name of the network"
  default     = "public209"
}

variable "plan_id" {
  type        = string
  description = "The chosen ID of the plan"
  default     = "eco-2-2-0"
}
