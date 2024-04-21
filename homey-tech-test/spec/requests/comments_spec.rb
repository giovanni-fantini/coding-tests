require 'rails_helper'

RSpec.describe "Comments", type: :request do
  let!(:user) { User.create(email: 'test@email.com', password: 'password') }
  let!(:project) { Project.create(name: 'Test Project', status: 'not_started') }

  describe 'POST /projects/1/comments' do
    context 'when the user is not logged in' do
      it 'redirects to the sign in page', :aggregate_failures do
        post "/projects/1/comments", params: { comment: { body: 'some comment' } }
        expect(response).to have_http_status(:found)
        expect(response).to redirect_to('/users/sign_in')
      end
    end

    context 'when the creation is succesful' do
      before { sign_in(user) }

      it 'redirects to the project show page', :aggregate_failures do
        post "/projects/1/comments", params: { comment: { body: 'some comment' } }
        expect(response).to have_http_status(:found)
        expect(response).to redirect_to('/projects/1')
      end

      it 'create the comment record', :aggregate_failures do
        post "/projects/1/comments", params: { comment: { body: 'some comment' } }
        expect(project.reload.comments.last.body).to eq('some comment')
      end
    end

    context 'when the update is not succesful' do
      before { sign_in(user) }

      it 'returns 422 and redirects to the project show page', :aggregate_failures do
        post "/projects/1/comments", params: { comment: { body: '' } }
        expect(response).to have_http_status(:unprocessable_entity)
        expect(response).to render_template(:show)
      end

      it "renders the error in the form" do
        post "/projects/1/comments", params: { comment: { body: '' } }
        expect(response.body).to include('Body can&#39;t be blank')
      end

      it 'does not create the comment record', :aggregate_failures do
        post "/projects/1/comments", params: { comment: { body: '' } }
        expect(project.reload.comments).to eq([])
      end
    end
  end
end

