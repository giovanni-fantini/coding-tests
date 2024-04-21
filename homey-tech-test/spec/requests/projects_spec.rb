require 'rails_helper'

RSpec.describe "Projects", type: :request do
  let(:user) { User.create(email: 'test@email.com', password: 'password') }
  let(:project) { Project.create(name: 'Test Project', status: 'not_started') }

  before do 
    Comment.create(project: project, user: user, body: 'This is the first comment')
    StatusChange.create(project: project, user: user, from: 'not_started', to: 'in_progress')
  end

  describe "GET /projects/1" do
    it "returns 200 and renders the show template", :aggregate_failures do
      get "/projects/1"
      expect(response).to have_http_status(:success)
      expect(response).to render_template(:show)
    end

    it "renders the comments and status changes history", :aggregate_failures do
      get "/projects/1"
      expect(response.body).to include('This is the first comment')
      expect(response.body).to include('Changed project status from not_started to in_progress')
    end
  end

  describe 'PATCH /projects/1' do
    context 'when the user is not logged in' do
      it 'redirects to the sign in page', :aggregate_failures do
        patch "/projects/1", params: { project: { status: 'done' } }
        expect(response).to have_http_status(:found)
        expect(response).to redirect_to('/users/sign_in')
      end
    end

    context 'when the update is succesful' do
      before { sign_in(user) }

      it 'redirects to the project show page', :aggregate_failures do
        patch "/projects/1", params: { project: { status: 'done' } }
        expect(response).to have_http_status(:found)
        expect(response).to redirect_to('/projects/1')
      end

      it 'updates the project record and creates a status_change record', :aggregate_failures do
        patch "/projects/1", params: { project: { status: 'done' } }
        expect(project.reload.status).to eq('done')
        expect(StatusChange.last.id).to eq(2)
      end
    end

    context 'when the update is not succesful' do
      before { sign_in(user) }

      it 'returns 422 and redirects to the project show page', :aggregate_failures do
        patch "/projects/1", params: { project: { status: 'something' } }
        expect(response).to have_http_status(:unprocessable_entity)
        expect(response).to render_template(:show)
      end

      it "renders the error in the form" do
        patch "/projects/1", params: { project: { status: 'something' } }
        expect(response.body).to include('Status is not included in the list')
      end

      it 'does not update the project record and create a status_change record', :aggregate_failures do
        patch "/projects/1", params: { project: { status: 'something' } }
        expect(project.reload.status).to eq('not_started')
        expect(StatusChange.last.id).to eq(1)
      end
    end
  end
end
