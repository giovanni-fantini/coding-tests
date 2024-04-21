puts 'Seeding initial values...'
homey_test = Project.create!(name: 'Homey Tech Test', status: 'not_started')
gio = User.create!(email: 'gio@example.com', password: 'password')
Comment.create!(user: gio, project: homey_test, body: 'Cool, I want to work on this - I will pick it up')
homey_test.update!(status: 'in_progress')
StatusChange.create!(user: gio, project: homey_test, from: homey_test.status, to: :in_progress)
puts 'Seeds added.'