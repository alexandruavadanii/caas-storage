# Copyright 2019 Nokia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

%define COMPONENT dynamic_local_pv_provisioner
%define RPM_NAME caas-%{COMPONENT}
%define RPM_MAJOR_VERSION 0.1.0
%define RPM_MINOR_VERSION 0
%define go_version 1.12.10
%define DEPENDENCY_MANAGER_VERSION 0.5.4
%define DYNAMIC_LOCAL_PV_PROVISIONER_VERSION 0e51e840742d412c877ab55e705e83b8f732e158
%define IMAGE_TAG %{RPM_MAJOR_VERSION}-%{RPM_MINOR_VERSION}
%define docker_build_dir %{_builddir}/%{RPM_NAME}-%{RPM_MAJOR_VERSION}/docker-build
%define docker_save_dir %{_builddir}/%{RPM_NAME}-%{RPM_MAJOR_VERSION}/docker-save

Name:           %{RPM_NAME}
Version:        %{RPM_MAJOR_VERSION}
Release:        %{RPM_MINOR_VERSION}%{?dist}
Summary:        Containers as a Service %{COMPONENT} component
License:        %{_platform_license} and GNU General Public License v2.0 only and MIT license and BSD 3-clause New or Revised License and MIT License and Curl License and BSD
URL:            https://github.com/nokia/dynamic-local-pv-provisioner
BuildArch:      %{_arch}
Vendor:         %{_platform_vendor} and nokia/dynamic-local-pv-provisioner unmodified
Source0:        %{name}-%{version}.tar.gz

Requires: docker-ce >= 18.09.2, rsync
BuildRequires: docker-ce-cli >= 18.09.2, xz

%description
This rpm contains the dynamic local pv provisioner container for caas subsystem.

%prep
%autosetup

%build
docker build \
  --network=host \
  --no-cache \
  --force-rm \
  --build-arg HTTP_PROXY="${http_proxy}" \
  --build-arg HTTPS_PROXY="${https_proxy}" \
  --build-arg NO_PROXY="${no_proxy}" \
  --build-arg http_proxy="${http_proxy}" \
  --build-arg https_proxy="${https_proxy}" \
  --build-arg no_proxy="${no_proxy}" \
  --build-arg DYNAMIC_LOCAL_PV_PROVISIONER_VERSION="%{DYNAMIC_LOCAL_PV_PROVISIONER_VERSION}" \
  --build-arg go_version="%{go_version}" \
  --build-arg DEPENDENCY_MANAGER_VERSION="%{DEPENDENCY_MANAGER_VERSION}" \
  --tag %{COMPONENT}:%{IMAGE_TAG} \
  %{docker_build_dir}/%{COMPONENT}/
mkdir -p %{docker_save_dir}/
docker save %{COMPONENT}:%{IMAGE_TAG} | xz -z -T2 > %{docker_save_dir}/%{COMPONENT}:%{IMAGE_TAG}.tar
docker rmi %{COMPONENT}:%{IMAGE_TAG}

%install
mkdir -p %{buildroot}/%{_caas_container_tar_path}
rsync -av %{docker_save_dir}/%{COMPONENT}:%{IMAGE_TAG}.tar %{buildroot}/%{_caas_container_tar_path}/

%files
%{_caas_container_tar_path}/%{COMPONENT}:%{IMAGE_TAG}.tar

%preun

%post

%postun

%clean
rm -rf ${buildroot}

