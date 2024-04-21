class CreateProjects < ActiveRecord::Migration[7.0]
  def change
    create_table :projects do |t|
      t.string :name
      t.string :status, default: 'not_started'

      t.timestamps
    end
  end
end
