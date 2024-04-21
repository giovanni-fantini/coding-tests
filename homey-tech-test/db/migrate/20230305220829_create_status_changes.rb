class CreateStatusChanges < ActiveRecord::Migration[7.0]
  def change
    create_table :status_changes do |t|
      t.string :from
      t.string :to
      t.references :project, null: false, foreign_key: true
      t.references :user, null: false, foreign_key: true, index: false

      t.timestamps
    end
  end
end
