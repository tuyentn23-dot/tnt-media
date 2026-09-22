"""Tests for Data Models"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import json
from src.models.channel import Channel
from src.models.content import Content
from src.models.ip import IP
from src.models.campaign import Campaign


class TestChannel:
    """Test Channel model"""
    
    def test_channel_creation(self):
        channel = Channel(
            channel_id="ch_001",
            name="Test Channel",
            platform="youtube"
        )
        assert channel.channel_id == "ch_001"
        assert channel.name == "Test Channel"
        assert channel.platform == "youtube"
        assert channel.is_active == True
    
    def test_channel_to_dict(self):
        channel = Channel(channel_id="ch_002", name="Test", platform="youtube")
        d = channel.to_dict()
        assert d["channel_id"] == "ch_002"
        assert d["name"] == "Test"
        assert "created_at" in d
    
    def test_channel_json_serialization(self):
        channel = Channel(channel_id="ch_003", name="Test", platform="youtube")
        json_str = channel.to_json()
        d = json.loads(json_str)
        assert d["channel_id"] == "ch_003"
        assert d["name"] == "Test"
    
    def test_channel_from_dict(self):
        data = {
            "channel_id": "ch_004",
            "name": "Test From Dict",
            "platform": "tiktok"
        }
        channel = Channel.from_dict(data)
        assert channel.channel_id == "ch_004"
        assert channel.name == "Test From Dict"
        assert channel.platform == "tiktok"


class TestContent:
    """Test Content model"""
    
    def test_content_creation(self):
        content = Content(
            content_id="cnt_001",
            title="Test Content",
            content_type="video"
        )
        assert content.content_id == "cnt_001"
        assert content.title == "Test Content"
        assert content.content_type == "video"
        assert content.status == "draft"
    
    def test_content_publish(self):
        content = Content(content_id="cnt_002", title="Test", content_type="video")
        content.publish()
        assert content.status == "published"
        assert content.published_at is not None
    
    def test_content_performance(self):
        content = Content(content_id="cnt_003", title="Test", content_type="video")
        content.update_performance({"views": 1000, "likes": 50})
        assert content.performance["views"] == 1000
        assert content.performance["likes"] == 50


class TestIP:
    """Test IP model"""
    
    def test_ip_creation(self):
        ip = IP(ip_id="ip_001", name="Test IP", ip_type="series")
        assert ip.ip_id == "ip_001"
        assert ip.name == "Test IP"
        assert ip.ip_type == "series"
    
    def test_ip_add_character(self):
        ip = IP(ip_id="ip_002", name="Test", ip_type="series")
        ip.add_character({"name": "Hero", "role": "main"})
        assert len(ip.characters) == 1
        assert ip.characters[0]["name"] == "Hero"


class TestCampaign:
    """Test Campaign model"""
    
    def test_campaign_creation(self):
        campaign = Campaign(
            campaign_id="cp_001",
            name="Test Campaign",
            objective="awareness"
        )
        assert campaign.campaign_id == "cp_001"
        assert campaign.name == "Test Campaign"
        assert campaign.objective == "awareness"
        assert campaign.status == "planned"
    
    def test_campaign_start(self):
        campaign = Campaign(campaign_id="cp_002", name="Test", objective="engagement")
        campaign.start()
        assert campaign.status == "active"
        assert campaign.start_date is not None


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
