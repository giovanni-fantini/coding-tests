class StatusChange < ApplicationRecord
  belongs_to :project
  belongs_to :user

  validates :from, presence: true, inclusion: { in: Project::STATUSES }
  validates :to, presence: true, inclusion: { in: Project::STATUSES }
end
