class Project < ApplicationRecord
  STATUSES = ['not_started', 'in_progress', 'done']

  has_many :comments
  has_many :status_changes

  validates :status, presence: true, inclusion: { in: STATUSES }

  def interaction_history
    (comments + status_changes).sort_by(&:created_at).reverse!
  end
end
