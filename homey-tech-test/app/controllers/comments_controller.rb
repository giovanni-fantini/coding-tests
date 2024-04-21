class CommentsController < ApplicationController
  before_action :authenticate_user!

  def create
    @project = Project.find(params[:project_id])
    @comment = @project.comments.new(comment_params)

    if @comment.save
      redirect_to project_path(@project), notice: 'Comment added succesfully!'
    else
      @interaction_history = @project.reload.interaction_history
      render "projects/show", status: :unprocessable_entity
    end
  end

  private

  def comment_params
    params.require(:comment).permit(:body).merge(user_id: current_user.id)
  end
end