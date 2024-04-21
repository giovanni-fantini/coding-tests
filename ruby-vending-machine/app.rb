# frozen_string_literal: true

require 'require_all'
require 'pry-byebug'
require_all 'lib'

VendingMachine::Computer.run
