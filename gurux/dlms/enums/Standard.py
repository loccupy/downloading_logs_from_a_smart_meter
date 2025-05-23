#
#  --------------------------------------------------------------------------
#   Gurux Ltd
#
#
#
#  Filename:        $HeadURL$
#
#  Version:         $Revision$,
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
from ..GXIntEnum import GXIntEnum

class Standard(GXIntEnum):
    """Used DLMS standard."""
    #pylint: disable=too-few-public-methods

    #Meter uses default DLMS IEC 62056 standard. https://dlms.com
    DLMS = 0
    #Meter uses India DLMS standard IS 15959-2. https://www.standardsbis.in
    INDIA = 1
    #Meter uses Italy DLMS standard UNI/TS 11291-11-2. https://uni.com
    ITALY = 2
    #Meter uses Saudi Arabia DLMS standard.
    SAUDI_ARABIA = 3
    #Meter uses IDIS DLMS standard. https://www.idis-association.com/
    IDIS = 4
    #Meter uses Spain DLMS standard.
    SPAIN = 5
