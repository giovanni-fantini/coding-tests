class ProjectsController < ApplicationController
  before_action :authenticate_user!, only: [:update]

  def index
    @projects = Project.all
  end

  def show
    @project = Project.find(params[:id])
    @interaction_history = @project.interaction_history
    @comment = @project.comments.build
  end

  def edit
    @project = Project.find(params[:id])
  end

  def update
    @project = Project.find(params[:id])
    current_status, new_status = @project.status, project_params[:status]

    if @project.update(project_params) && @project.status_changes.create(user: current_user, from: current_status, to: new_status)
      redirect_to @project, notice: 'Project updated succesfully!'
    else
      @interaction_history = @project.interaction_history
      @comment = @project.comments.build
      render action: :show, status: :unprocessable_entity
    end
  end

  private

  def project_params
    params.require(:project).permit(:status)
  end
end
