#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename: $HeadURL$
#
#  Version: $Revision$,
#                   $Date$
#                   $Author$
#
#  Copyright (c) Gurux Ltd
#
# ---------------------------------------------------------------------------
#
#   DESCRIPTION
#
#  This file is a part of Gurux Device Framework.
#
#  Gurux Device Framework is Open Source software; you can redistribute it
#  and/or modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; version 2 of the License.
#  Gurux Device Framework is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#  See the GNU General Public License for more details.
#
#  More information of Gurux products: http://www.gurux.org
#
#  This code is licensed under the GNU General Public License v2.
#  Full text may be retrieved at http://www.gnu.org/licenses/gpl-2.0.txt
# ---------------------------------------------------------------------------
from libs.gurux.dlms.GXIntFlag import GXIntFlag

class Weekdays(GXIntFlag):
    """
    Defines the weekdays.
    """
    #pylint: disable=too-few-public-methods

    #
    # Indicates Monday.
    #
    NONE = 0x0

    #
    # Indicates Monday.
    #
    MONDAY = 0x1
    #
    # Indicates Tuesday.
    #
    TUESDAY = 0x2
    #
    # Indicates Wednesday.
    #
    WEDNESDAY = 0x4
    #
    # Indicates Thursday.
    #
    THURSDAY = 0x8
    #
    # Indicates Friday.
    #
    FRIDAY = 0x10
    #
    # Indicates Saturday.
    #
    SATURDAY = 0x20
    #
    # Indicates Sunday.
    #
    SUNDAY = 0x40
