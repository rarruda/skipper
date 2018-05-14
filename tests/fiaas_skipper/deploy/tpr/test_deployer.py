#!/usr/bin/env python
# -*- coding: utf-8
import mock
import pytest

from fiaas_skipper import TprDeployer
from fiaas_skipper.deploy.channel import ReleaseChannel
from fiaas_skipper.deploy.tpr.types import PaasbetaApplicationSpec
from fiaas_skipper.deploy.deploy import DeploymentConfig


class TestTprDeployer(object):
    @pytest.fixture
    def cluster(self):
        cluster = mock.NonCallableMagicMock(name="cluster")
        cluster.find_deployment_configs.return_value = (
            DeploymentConfig("testapp", "test1", "stable"),
        )
        return cluster

    @pytest.fixture
    def release_channel_factory(self):
        release_channel_factory = mock.MagicMock(name="release_channel_factory")
        release_channel_factory.return_value = ReleaseChannel(name="xx", tag="stable", metadata={"image": "image1"})
        return release_channel_factory

    @mock.patch('fiaas_skipper.deploy.tpr.types.PaasbetaApplication.get_or_create', autospec=True)
    def test_deploy_creates_paasbeta_application(self, get_or_create, cluster, release_channel_factory):
        app = mock.MagicMock()
        spec = mock.PropertyMock()
        type(app).spec = spec
        get_or_create.return_value = app
        bootstrap = mock.MagicMock()
        spec_config = {"x": "x"}
        deployer = TprDeployer(cluster, release_channel_factory, bootstrap, spec_config=spec_config)
        deployer.deploy()
        spec.assert_called_once_with(PaasbetaApplicationSpec(application="testapp", image="image1", config=spec_config))
        app.save.assert_called_once()